from django import forms
from .models import Order, OrderWorkJournal, FurnitureType, Workshop, Worker


class OrderForm(forms.ModelForm):
    """Форма для создания и редактирования заказа."""
    
    class Meta:
        model = Order
        fields = (
            'title', 'description', 'customer_name', 'customer_phone',
            'furniture_type', 'workshops', 'status', 'priority',
            'deadline', 'total_cost', 'notes'
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 7}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'furniture_type': forms.Select(attrs={'class': 'form-control'}),
            'workshops': forms.CheckboxSelectMultiple(),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class OrderWorkJournalForm(forms.ModelForm):
    """Форма для создания и редактирования записи журнала работы."""
    
    class Meta:
        model = OrderWorkJournal
        fields = ('workshop', 'workers', 'start_time', 'end_time', 'work_description')
        widgets = {
            'workshop': forms.Select(attrs={'class': 'form-control'}),
            'workers': forms.CheckboxSelectMultiple(),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'work_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FurnitureTypeForm(forms.ModelForm):
    """Форма для создания и редактирования типа мебели."""
    
    class Meta:
        model = FurnitureType
        fields = ('title', 'description', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class WorkshopForm(forms.ModelForm):
    """Форма для создания и редактирования цеха."""
    
    class Meta:
        model = Workshop
        fields = ('title', 'description', 'workshop_number', 'supervisor')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'workshop_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'supervisor': forms.Select(attrs={'class': 'form-control'}),
        }


class WorkerForm(forms.ModelForm):
    """Форма для создания и редактирования рабочего."""
    
    class Meta:
        model = Worker
        fields = ('first_name', 'last_name', 'patronymic', 'position', 'workshop', 'hire_date')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'workshop': forms.Select(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

