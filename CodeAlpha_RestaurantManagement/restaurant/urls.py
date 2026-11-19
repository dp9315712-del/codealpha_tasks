from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_list, name='menu-list'),
    path('menu/<int:pk>/', views.menu_detail, name='menu-detail'),
    path('orders/', views.order_list, name='order-list'),
    path('tables/', views.table_list, name='table-list'),
    path('tables/available/', views.available_tables, name='available-tables'),
    path('reservations/', views.reservation_create, name='reservation-create'),
    path('inventory/', views.inventory_list, name='inventory-list'),
    path('inventory/<int:pk>/', views.inventory_detail, name='inventory-detail'),
]