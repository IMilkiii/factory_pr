"""
Скрипт для создания тестовых данных мебельной фабрики.
Запуск: python manage.py shell < create_sample_data.py
Или: python manage.py shell, затем скопировать код
"""
import os
import django
from datetime import timedelta, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'factory.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from exhibits.models import FurnitureType, Workshop, Worker, Order, OrderWorkJournal

User = get_user_model()

# Создаем пользователя, если его нет
user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@factory.ru',
        'first_name': 'Администратор',
        'last_name': 'Фабрики',
        'is_staff': True,
        'is_superuser': True,
    }
)
if created:
    user.set_password('admin123')
    user.save()
    print(f'Создан пользователь: {user.username}')
else:
    print(f'Пользователь уже существует: {user.username}')

# Создаем типы мебели
sofa, _ = FurnitureType.objects.get_or_create(
    title='Диван',
    defaults={
        'description': 'Мягкая мебель для гостиной',
        'category': 'upholstered'
    }
)
armchair, _ = FurnitureType.objects.get_or_create(
    title='Кресло',
    defaults={
        'description': 'Удобное кресло для отдыха',
        'category': 'upholstered'
    }
)
wardrobe, _ = FurnitureType.objects.get_or_create(
    title='Шкаф',
    defaults={
        'description': 'Корпусная мебель для хранения одежды',
        'category': 'case'
    }
)
table, _ = FurnitureType.objects.get_or_create(
    title='Обеденный стол',
    defaults={
        'description': 'Стол для столовой',
        'category': 'case'
    }
)
kitchen_set, _ = FurnitureType.objects.get_or_create(
    title='Кухонный гарнитур',
    defaults={
        'description': 'Мебель для кухни',
        'category': 'kitchen'
    }
)

# Создаем цеха
workshop1, _ = Workshop.objects.get_or_create(
    workshop_number=1,
    defaults={
        'title': 'Цех мягкой мебели',
        'description': 'Производство диванов, кресел и другой мягкой мебели',
        'supervisor': user
    }
)
workshop2, _ = Workshop.objects.get_or_create(
    workshop_number=2,
    defaults={
        'title': 'Цех корпусной мебели',
        'description': 'Изготовление шкафов, столов и другой корпусной мебели',
        'supervisor': user
    }
)
workshop3, _ = Workshop.objects.get_or_create(
    workshop_number=3,
    defaults={
        'title': 'Сборочный цех',
        'description': 'Финальная сборка и отделка мебели',
        'supervisor': user
    }
)

# Создаем рабочих
worker1, _ = Worker.objects.get_or_create(
    first_name='Иван',
    last_name='Петров',
    defaults={
        'patronymic': 'Сергеевич',
        'position': 'Мастер по мягкой мебели',
        'workshop': workshop1,
        'hire_date': date(2020, 3, 15)
    }
)

worker2, _ = Worker.objects.get_or_create(
    first_name='Мария',
    last_name='Иванова',
    defaults={
        'patronymic': 'Алексеевна',
        'position': 'Сборщик мебели',
        'workshop': workshop2,
        'hire_date': date(2019, 7, 22)
    }
)

worker3, _ = Worker.objects.get_or_create(
    first_name='Алексей',
    last_name='Сидоров',
    defaults={
        'patronymic': 'Викторович',
        'position': 'Отделочник',
        'workshop': workshop3,
        'hire_date': date(2021, 1, 10)
    }
)

worker4, _ = Worker.objects.get_or_create(
    first_name='Елена',
    last_name='Козлова',
    defaults={
        'patronymic': 'Дмитриевна',
        'position': 'Швея',
        'workshop': workshop1,
        'hire_date': date(2020, 11, 5)
    }
)

# Создаем заказы
order1, created = Order.objects.get_or_create(
    title='Диван "Уютный" для гостиной',
    defaults={
        'description': 'Большой угловой диван с механизмом трансформации. Обивка из велюра, наполнитель - пенополиуретан.',
        'customer_name': 'Анна Смирнова',
        'customer_phone': '+7(916)123-45-67',
        'furniture_type': sofa,
        'status': 'in_progress',
        'priority': 'high',
        'deadline': date.today() + timedelta(days=14),
        'total_cost': 45000.00,
        'notes': 'Срочный заказ, клиент переезжает в новую квартиру'
    }
)
if created:
    order1.workshops.add(workshop1, workshop3)
    print(f'Создан заказ: {order1.title}')

order2, created = Order.objects.get_or_create(
    title='Шкаф-купе "Спейс"',
    defaults={
        'description': 'Встроенный шкаф-купе с зеркальными дверцами. Внутреннее наполнение по индивидуальному проекту.',
        'customer_name': 'Михаил Волков',
        'customer_phone': '+7(903)987-65-43',
        'furniture_type': wardrobe,
        'status': 'new',
        'priority': 'medium',
        'deadline': date.today() + timedelta(days=21),
        'total_cost': 35000.00,
        'notes': 'Требуется точная замеровка на месте'
    }
)
if created:
    order2.workshops.add(workshop2, workshop3)
    print(f'Создан заказ: {order2.title}')

order3, created = Order.objects.get_or_create(
    title='Кухонный гарнитур "Модерн"',
    defaults={
        'description': 'Современный кухонный гарнитур с фасадами МДФ. Столешница из кварца. Встроенная техника.',
        'customer_name': 'Ольга Новикова',
        'customer_phone': '+7(926)456-78-90',
        'furniture_type': kitchen_set,
        'status': 'completed',
        'priority': 'low',
        'deadline': date.today() - timedelta(days=5),
        'completion_date': date.today() - timedelta(days=3),
        'total_cost': 85000.00,
        'notes': 'Заказ успешно выполнен и доставлен клиенту'
    }
)
if created:
    order3.workshops.add(workshop2, workshop3)
    print(f'Создан заказ: {order3.title}')

order4, created = Order.objects.get_or_create(
    title='Обеденный стол с 6 стульями',
    defaults={
        'description': 'Массивный обеденный стол из дуба с 6 стульями. Классический дизайн.',
        'customer_name': 'Дмитрий Соколов',
        'customer_phone': '+7(915)234-56-78',
        'furniture_type': table,
        'status': 'in_progress',
        'priority': 'medium',
        'deadline': date.today() + timedelta(days=10),
        'total_cost': 28000.00,
        'notes': 'Дерево уже подготовлено, начинается сборка'
    }
)
if created:
    order4.workshops.add(workshop2, workshop3)
    print(f'Создан заказ: {order4.title}')

# Создаем записи в журнале работы
if order1.status == 'in_progress':
    journal1, created = OrderWorkJournal.objects.get_or_create(
        order=order1,
        workshop=workshop1,
        defaults={
            'start_time': timezone.now() - timedelta(hours=8),
            'end_time': timezone.now() - timedelta(hours=4),
            'work_description': 'Изготовление каркаса дивана, установка пружинного блока'
        }
    )
    if created:
        journal1.workers.add(worker1, worker4)
        print(f'Создана запись в журнале: {journal1}')

if order4.status == 'in_progress':
    journal2, created = OrderWorkJournal.objects.get_or_create(
        order=order4,
        workshop=workshop2,
        defaults={
            'start_time': timezone.now() - timedelta(hours=6),
            'end_time': timezone.now() - timedelta(hours=2),
            'work_description': 'Сборка столешницы и ножек стола, финальная отделка'
        }
    )
    if created:
        journal2.workers.add(worker2)
        print(f'Создана запись в журнале: {journal2}')

print('\nТестовые данные успешно созданы!')
print(f'Всего типов мебели: {FurnitureType.objects.count()}')
print(f'Всего цехов: {Workshop.objects.count()}')
print(f'Всего рабочих: {Worker.objects.count()}')
print(f'Всего заказов: {Order.objects.count()}')
print(f'Всего записей в журнале: {OrderWorkJournal.objects.count()}')
