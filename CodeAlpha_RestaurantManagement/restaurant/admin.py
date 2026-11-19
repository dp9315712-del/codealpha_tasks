from django.contrib import admin
from .models import (
    MenuItem,
    DiningTable,
    Inventory,
    Reservation,
    Order,
    OrderItem
)

admin.site.register(MenuItem)
admin.site.register(DiningTable)
admin.site.register(Inventory)
admin.site.register(Reservation)
admin.site.register(Order)
admin.site.register(OrderItem)