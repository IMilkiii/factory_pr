from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count
from exhibits.models import Order
from .forms import CreationForm

User = get_user_model()


def signup(request):
    """Регистрация нового пользователя."""
    form = CreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'users/signup.html', {'form': form})


def profile(request, username):
    """Страница профиля пользователя."""
    user = get_object_or_404(User, username=username)
    
    # Администратор видит все заказы, остальные - только свои
    if request.user == user or request.user.is_superuser:
        order_list = Order.objects.all().annotate(
            workshop_count=Count('workshops')
        )
    else:
        order_list = Order.objects.filter(
            # Здесь можно добавить фильтрацию по заказам пользователя
        ).annotate(
            workshop_count=Count('workshops')
        )
    
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile_user': user,
        'page_obj': page_obj,
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_edit(request):
    """Редактирование профиля."""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.username = request.POST.get('username', '')
        user.email = request.POST.get('email', '')
        user.save()
        return redirect('users:profile', username=user.username)
    
    return render(request, 'users/profile_edit.html')
