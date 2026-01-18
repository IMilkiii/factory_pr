from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

User = get_user_model()


class ActiveManager(models.Manager):
    """Менеджер для получения активных заказов."""
    
    def get_queryset(self):
        return super().get_queryset().filter(
            status='in_progress'
        )


class BaseModel(models.Model):
    """Абстрактная базовая модель с общими полями."""
    
    title = models.CharField(
        'Название',
        max_length=256
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    
    class Meta:
        abstract = True
        ordering = ('title',)


class FurnitureType(BaseModel):
    """Модель типа мебели."""
    
    FURNITURE_CATEGORIES = [
        ('upholstered', 'Мягкая мебель'),
        ('case', 'Корпусная мебель'),
        ('office', 'Офисная мебель'),
        ('kitchen', 'Кухонная мебель'),
    ]
    
    category = models.CharField(
        'Категория',
        max_length=20,
        choices=FURNITURE_CATEGORIES,
        default='case'
    )
    
    class Meta:
        verbose_name = 'Тип мебели'
        verbose_name_plural = 'Типы мебели'
        ordering = ('category', 'title')
    
    def __str__(self):
        return f'{self.title} ({self.get_category_display()})'


class Workshop(BaseModel):
    """Модель цеха."""
    
    workshop_number = models.PositiveSmallIntegerField(
        'Номер цеха',
        unique=True
    )
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='supervised_workshops',
        verbose_name='Начальник цеха'
    )
    
    class Meta:
        verbose_name = 'Цех'
        verbose_name_plural = 'Цеха'
        ordering = ('workshop_number',)
    
    def __str__(self):
        return f'Цех {self.workshop_number}: {self.title}'


class Worker(models.Model):
    """Модель рабочего."""
    
    first_name = models.CharField(
        'Имя',
        max_length=100
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=100
    )
    patronymic = models.CharField(
        'Отчество',
        max_length=100,
        blank=True
    )
    position = models.CharField(
        'Должность',
        max_length=100
    )
    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        related_name='workers',
        verbose_name='Цех'
    )
    hire_date = models.DateField(
        'Дата приема на работу',
        default=timezone.now
    )
    
    class Meta:
        verbose_name = 'Рабочий'
        verbose_name_plural = 'Рабочие'
        ordering = ('last_name', 'first_name')
    
    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'
    
    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'


class Order(BaseModel):
    """Модель заказа."""
    
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('urgent', 'Срочный'),
    ]
    
    customer_name = models.CharField(
        'Имя заказчика',
        max_length=200
    )
    customer_phone = models.CharField(
        'Телефон заказчика',
        max_length=20
    )
    furniture_type = models.ForeignKey(
        FurnitureType,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Тип мебели'
    )
    workshops = models.ManyToManyField(
        Workshop,
        related_name='orders',
        verbose_name='Цеха для выполнения'
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    priority = models.CharField(
        'Приоритет',
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    deadline = models.DateField(
        'Срок выполнения',
        help_text='Планируемая дата завершения заказа'
    )
    completion_date = models.DateField(
        'Дата фактического выполнения',
        null=True,
        blank=True
    )
    total_cost = models.DecimalField(
        'Общая стоимость',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    notes = models.TextField(
        'Примечания',
        blank=True
    )
    
    objects = models.Manager()
    active = ActiveManager()
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_at',)
    
    def __str__(self):
        return f'Заказ #{self.id}: {self.title}'
    
    def is_overdue(self):
        """Проверяет, просрочен ли заказ."""
        return (
            self.status in ['new', 'in_progress'] and
            self.deadline < timezone.now().date()
        )
    
    def mark_completed(self):
        """Отмечает заказ как выполненный."""
        self.status = 'completed'
        self.completion_date = timezone.now().date()
        self.save()


class OrderWorkJournal(models.Model):
    """Модель журнала работы над заказами."""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='work_journal',
        verbose_name='Заказ'
    )
    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        related_name='work_journal',
        verbose_name='Цех'
    )
    workers = models.ManyToManyField(
        Worker,
        related_name='work_journal',
        verbose_name='Рабочие'
    )
    start_time = models.DateTimeField(
        'Начало работы',
        default=timezone.now
    )
    end_time = models.DateTimeField(
        'Окончание работы',
        null=True,
        blank=True
    )
    work_description = models.TextField(
        'Описание выполненных работ',
        blank=True
    )
    
    class Meta:
        verbose_name = 'Запись журнала работы'
        verbose_name_plural = 'Журнал работы'
        ordering = ('-start_time',)
    
    def __str__(self):
        return f'{self.order.title} - {self.workshop.title}'


class OrderPhoto(models.Model):
    """Модель фотографий заказа."""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Заказ'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='orders/photos/'
    )
    description = models.CharField(
        'Описание',
        max_length=256,
        blank=True
    )
    created_at = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Фотография заказа'
        verbose_name_plural = 'Фотографии заказа'
        ordering = ('-created_at',)
    
    def __str__(self):
        return f'Фото заказа {self.order.title}'

