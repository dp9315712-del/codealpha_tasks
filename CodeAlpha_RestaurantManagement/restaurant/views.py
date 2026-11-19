from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from datetime import timedelta
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import (
    MenuItem,
    Order,
    OrderItem,
    Inventory,
    DiningTable,
    Reservation
)

from .serializers import (
    MenuItemSerializer,
    OrderSerializer,
    DiningTableSerializer,
    ReservationSerializer,
    InventorySerializer
)


# GET: View all menu items
@api_view(['GET'])
def menu_list(request):
    menu_items = MenuItem.objects.all()
    serializer = MenuItemSerializer(menu_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# GET: View single menu item
@api_view(['GET'])
def menu_detail(request, pk):
    try:
        menu_item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response(
            {"error": "Menu item not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = MenuItemSerializer(menu_item)
    return Response(serializer.data, status=status.HTTP_200_OK)


# GET: View all orders
# POST: Place a new order
@transaction.atomic
@api_view(['GET', 'POST'])
def order_list(request):

    if request.method == 'GET':
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    customer_name = request.data.get('customer_name')
    table_id = request.data.get('table')
    items = request.data.get('items')

    if not customer_name or not isinstance(customer_name, str):
        return Response(
            {"error": "Customer name is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not isinstance(items, list) or not items:
        return Response(
            {"error": "Order items are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        table = None

        if table_id is not None:
            table = DiningTable.objects.get(pk=table_id)

        item_details = []
        seen_items = set()

        for item in items:

            if not isinstance(item, dict):
                return Response(
                    {"error": "Invalid order item"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            menu_id = item.get('menu_item')
            quantity = item.get('quantity')

            if (
                not isinstance(menu_id, int)
                or isinstance(menu_id, bool)
                or not isinstance(quantity, int)
                or isinstance(quantity, bool)
                or quantity <= 0
            ):
                return Response(
                    {"error": "Invalid menu item or quantity"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if menu_id in seen_items:
                return Response(
                    {"error": "Duplicate menu items are not allowed"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            seen_items.add(menu_id)

            menu_item = MenuItem.objects.get(pk=menu_id)

            if not menu_item.is_available:
                return Response(
                    {"error": f"{menu_item.name} is not available"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            inventory = Inventory.objects.select_for_update().get(
                menu_item=menu_item
            )

            if inventory.quantity < quantity:
                return Response(
                    {
                        "error": f"Insufficient stock for {menu_item.name}",
                        "available_stock": inventory.quantity
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            item_details.append((menu_item, inventory, quantity))

        total = 0

        order = Order.objects.create(
            customer_name=customer_name,
            table=table
        )

        for menu_item, inventory, quantity in item_details:

            unit_price = menu_item.price
            total += unit_price * quantity

            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                unit_price=unit_price
            )

            inventory.quantity -= quantity
            inventory.save()

        order.total_amount = total
        order.save()

        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    except DiningTable.DoesNotExist:
        return Response(
            {"error": "Table not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except MenuItem.DoesNotExist:
        return Response(
            {"error": "Menu item not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except Inventory.DoesNotExist:
        return Response(
            {"error": "Inventory record not found for menu item"},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def table_list(request):
    tables = DiningTable.objects.all().order_by('table_number')
    serializer = DiningTableSerializer(tables, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def available_tables(request):
    reservation_time = request.GET.get('reservation_time')
    guests = request.GET.get('guests')

    if not reservation_time or not guests:
        return Response(
            {"error": "reservation_time and guests are required"},
            status=400
        )

    try:
        guests = int(guests)

        if guests < 1:
            return Response(
                {"error": "Guests must be at least 1"},
                status=400
            )

    except ValueError:
        return Response(
            {"error": "Guests must be a valid number"},
            status=400
        )

    requested_time = parse_datetime(reservation_time)

    if requested_time is None:
        return Response(
            {"error": "Invalid reservation_time format"},
            status=400
        )

    if timezone.is_naive(requested_time):
        requested_time = timezone.make_aware(requested_time)

    duration = timedelta(hours=2)

    start_time = requested_time - duration
    end_time = requested_time + duration

    tables = DiningTable.objects.filter(
        is_available=True,
        capacity__gte=guests
    ).exclude(
        reservations__status='Confirmed',
        reservations__reservation_time__gt=start_time,
        reservations__reservation_time__lt=end_time
    ).distinct().order_by('table_number')

    serializer = DiningTableSerializer(tables, many=True)

    return Response({
        "reservation_time": reservation_time,
        "guests": guests,
        "available_tables": serializer.data
    })


@transaction.atomic
@api_view(['GET', 'POST'])
def reservation_create(request):

    # GET: View all reservations
    if request.method == 'GET':
        reservations = Reservation.objects.all().order_by('-created_at')

        serializer = ReservationSerializer(
            reservations,
            many=True
        )

        return Response(serializer.data)

    # POST: Create a new reservation
    serializer = ReservationSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    table = serializer.validated_data['table']
    reservation_time = serializer.validated_data['reservation_time']
    guests = serializer.validated_data['guests']

    # Check table availability
    if not table.is_available:
        return Response(
            {"error": "This table is not available"},
            status=400
        )

    # Check guest capacity
    if guests > table.capacity:
        return Response(
            {"error": "Guest count exceeds table capacity"},
            status=400
        )

    # Check duplicate reservation within 2 hours
    start_time = reservation_time - timedelta(hours=2)
    end_time = reservation_time + timedelta(hours=2)

    existing_reservation = Reservation.objects.filter(
        table=table,
        status='Confirmed',
        reservation_time__gt=start_time,
        reservation_time__lt=end_time
    ).exists()

    if existing_reservation:
        return Response(
            {"error": "This table is already reserved for this time"},
            status=400
        )

    reservation = serializer.save()

    return Response(
        ReservationSerializer(reservation).data,
        status=201
    )

# GET: View all inventory records
@api_view(['GET'])
def inventory_list(request):
    inventory = Inventory.objects.all().order_by('id')
    serializer = InventorySerializer(inventory, many=True)
    return Response(serializer.data)


# GET: View single inventory
# PATCH: Update inventory
@api_view(['GET', 'PATCH'])
def inventory_detail(request, pk):

    try:
        inventory = Inventory.objects.get(pk=pk)
    except Inventory.DoesNotExist:
        return Response(
            {"error": "Inventory record not found"},
            status=404
        )

    if request.method == 'GET':
        serializer = InventorySerializer(inventory)
        return Response(serializer.data)

    serializer = InventorySerializer(
        inventory,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)