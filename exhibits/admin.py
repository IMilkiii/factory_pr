from django.contrib import admin
from .models import FurnitureType, Workshop, Worker, Order, OrderPhoto, OrderWorkJournal


@admin.register(FurnitureType)
class FurnitureTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('category', 'created_at')


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('workshop_number', 'title', 'supervisor', 'created_at')
    search_fields = ('title', 'workshop_number')
    list_filter = ('supervisor', 'created_at')
    raw_id_fields = ('supervisor',)


class WorkerInline(admin.TabularInline):
    model = Worker
    extra = 0


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'position', 'workshop', 'hire_date')
    search_fields = ('last_name', 'first_name', 'patronymic', 'position')
    list_filter = ('workshop', 'hire_date', 'position')
    raw_id_fields = ('workshop',)


class OrderPhotoInline(admin.TabularInline):
    model = OrderPhoto
    extra = 0


class OrderWorkJournalInline(admin.TabularInline):
    model = OrderWorkJournal
    extra = 0
    raw_id_fields = ('workshop', 'workers')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer_name', 'furniture_type', 'status', 'priority', 'deadline', 'is_overdue')
    list_editable = ('status', 'priority')
    search_fields = ('title', 'description', 'customer_name')
    list_filter = ('status', 'priority', 'furniture_type', 'deadline', 'created_at')
    raw_id_fields = ('furniture_type',)
    filter_horizontal = ('workshops',)
    date_hierarchy = 'deadline'
    inlines = (OrderPhotoInline, OrderWorkJournalInline)
    
    def is_overdue(self, obj):
        return obj.is_overdue()
    is_overdue.boolean = True
    is_overdue.short_description = 'Просрочен'


@admin.register(OrderPhoto)
class OrderPhotoAdmin(admin.ModelAdmin):
    list_display = ('order', 'description', 'created_at')
    search_fields = ('order__title', 'description')
    list_filter = ('created_at',)
    raw_id_fields = ('order',)


@admin.register(OrderWorkJournal)
class OrderWorkJournalAdmin(admin.ModelAdmin):
    list_display = ('order', 'workshop', 'start_time', 'end_time')
    search_fields = ('order__title', 'work_description')
    list_filter = ('workshop', 'start_time', 'end_time')
    raw_id_fields = ('order', 'workshop')
    filter_horizontal = ('workers',)
    date_hierarchy = 'start_time'

