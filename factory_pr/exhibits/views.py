from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.http import Http404
from django.db.models import Count, Q
from django.utils import timezone
from .models import Order, FurnitureType, Workshop, Worker, OrderWorkJournal
from .forms import OrderForm, OrderWorkJournalForm

User = get_user_model()


def get_active_orders():
    """Получить активные заказы."""
    return Order.active.select_related('furniture_type')


def index(request):
    """Главная страница со списком заказов."""
    order_list = get_active_orders().annotate(
        workshop_count=Count('workshops')
    )
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'exhibits/index.html', context)


def order_detail(request, order_id):
    """Страница детального просмотра заказа."""
    order = get_object_or_404(
        Order.objects.select_related('furniture_type').prefetch_related('workshops', 'photos'),
        pk=order_id
    )
    
    work_journal = order.work_journal.select_related('workshop').prefetch_related('workers').all()
    form = None
    edit_journal_id = request.GET.get('edit_journal')
    delete_journal_id = request.GET.get('delete_journal')
    journal_to_edit = None
    journal_to_delete = None
    
    if request.user.is_authenticated:
        if edit_journal_id:
            journal_to_edit = get_object_or_404(OrderWorkJournal, pk=edit_journal_id, order=order)
            form = OrderWorkJournalForm(instance=journal_to_edit)
        else:
            form = OrderWorkJournalForm()
        
        if delete_journal_id:
            journal_to_delete = get_object_or_404(OrderWorkJournal, pk=delete_journal_id, order=order)
    
    context = {
        'order': order,
        'work_journal': work_journal,
        'form': form,
        'journal_to_edit': journal_to_edit,
        'journal_to_delete': journal_to_delete,
    }
    return render(request, 'exhibits/order_detail.html', context)


def furniture_type_list(request):
    """Список типов мебели."""
    furniture_types = FurnitureType.objects.annotate(
        order_count=Count('orders')
    )
    paginator = Paginator(furniture_types, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'exhibits/furniture_type_list.html', context)


def furniture_type_detail(request, furniture_type_id):
    """Детальная страница типа мебели."""
    furniture_type = get_object_or_404(FurnitureType, pk=furniture_type_id)
    order_list = get_active_orders().filter(
        furniture_type=furniture_type
    ).annotate(
        workshop_count=Count('workshops')
    )
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'furniture_type': furniture_type,
        'page_obj': page_obj,
    }
    return render(request, 'exhibits/furniture_type_detail.html', context)


def workshop_list(request):
    """Список цехов."""
    workshops = Workshop.objects.select_related('supervisor').annotate(
        worker_count=Count('workers'),
        active_order_count=Count('orders', filter=Q(orders__status='in_progress'))
    )
    paginator = Paginator(workshops, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'exhibits/workshop_list.html', context)


def workshop_detail(request, workshop_id):
    """Детальная страница цеха."""
    workshop = get_object_or_404(
        Workshop.objects.select_related('supervisor').prefetch_related('workers'),
        pk=workshop_id
    )
    workers = workshop.workers.all()
    orders = workshop.orders.filter(status='in_progress').select_related('furniture_type')
    context = {
        'workshop': workshop,
        'workers': workers,
        'orders': orders,
    }
    return render(request, 'exhibits/workshop_detail.html', context)


@login_required
def order_create(request):
    """Создание нового заказа."""
    form = OrderForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        order = form.save(commit=False)
        order.save()
        form.save_m2m()
        return redirect('exhibits:order_detail', order_id=order.id)
    return render(request, 'exhibits/order_form.html', {'form': form})


@login_required
def order_edit(request, order_id):
    """Редактирование заказа."""
    order = get_object_or_404(Order, pk=order_id)
    
    form = OrderForm(request.POST or None, request.FILES or None, instance=order)
    if form.is_valid():
        form.save()
        return redirect('exhibits:order_detail', order_id=order.id)
    return render(request, 'exhibits/order_form.html', {'form': form, 'order': order})


@login_required
@require_http_methods(['GET', 'POST'])
def order_delete(request, order_id):
    """Удаление заказа."""
    order = get_object_or_404(Order, pk=order_id)
    
    if request.method == 'POST':
        order.delete()
        return redirect('exhibits:index')
    
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect(f'/orders/{order_id}/?delete=1')


@login_required
@require_http_methods(['POST'])
def add_work_journal(request, order_id):
    """Добавление записи в журнал работы."""
    order = get_object_or_404(Order, pk=order_id)
    form = OrderWorkJournalForm(request.POST)
    if form.is_valid():
        journal = form.save(commit=False)
        journal.order = order
        journal.save()
        form.save_m2m()
    return redirect('exhibits:order_detail', order_id=order_id)


@login_required
@require_http_methods(['GET', 'POST'])
def edit_work_journal(request, order_id, journal_id):
    """Редактирование записи журнала работы."""
    order = get_object_or_404(Order, pk=order_id)
    journal = get_object_or_404(OrderWorkJournal, pk=journal_id, order=order)
    
    form = OrderWorkJournalForm(request.POST or None, instance=journal)
    if form.is_valid():
        form.save()
        return redirect('exhibits:order_detail', order_id=order_id)
    
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect(f'/orders/{order_id}/?edit_journal={journal_id}')


@login_required
@require_http_methods(['GET', 'POST'])
def delete_work_journal(request, order_id, journal_id):
    """Удаление записи журнала работы."""
    order = get_object_or_404(Order, pk=order_id)
    journal = get_object_or_404(OrderWorkJournal, pk=journal_id, order=order)
    
    if request.method == 'POST':
        journal.delete()
        return redirect('exhibits:order_detail', order_id=order_id)
    
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect(f'/orders/{order_id}/?delete_journal={journal_id}')


@login_required
def complete_order(request, order_id):
    """Завершение заказа."""
    order = get_object_or_404(Order, pk=order_id)
    order.mark_completed()
    return redirect('exhibits:order_detail', order_id=order_id)

