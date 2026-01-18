from django.urls import path
from . import views

app_name = 'exhibits'

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:order_id>/edit/', views.order_edit, name='order_edit'),
    path('orders/<int:order_id>/delete/', views.order_delete, name='order_delete'),
    path('orders/<int:order_id>/complete/', views.complete_order, name='complete_order'),
    path('orders/<int:order_id>/work_journal/', views.add_work_journal, name='add_work_journal'),
    path('orders/<int:order_id>/edit_journal/<int:journal_id>/', views.edit_work_journal, name='edit_work_journal'),
    path('orders/<int:order_id>/delete_journal/<int:journal_id>/', views.delete_work_journal, name='delete_work_journal'),
    path('furniture-types/', views.furniture_type_list, name='furniture_type_list'),
    path('furniture-types/<int:furniture_type_id>/', views.furniture_type_detail, name='furniture_type_detail'),
    path('workshops/', views.workshop_list, name='workshop_list'),
    path('workshops/<int:workshop_id>/', views.workshop_detail, name='workshop_detail'),
]

