# Restaurant Management System

## Project Overview
The Restaurant Management System is a backend application developed using Python, Django, and Django REST Framework. It helps manage restaurant menu items, dining tables, inventory, reservations, and customer orders.

## Technologies Used
- Python
- Django
- Django REST Framework
- SQLite

## Features
- View restaurant menu items
- View dining tables
- Check table availability
- Create and view reservations
- Prevent duplicate reservations
- Validate table capacity
- Create and view customer orders
- Calculate order totals
- Automatically decrease inventory stock when an order is placed
- Prevent orders when stock is insufficient
- View inventory details
- Update inventory quantities

## Database Models
- MenuItem
- DiningTable
- Inventory
- Reservation
- Order
- OrderItem

## API Functionality
The project provides REST API endpoints for:
- Menu management
- Dining table management
- Table availability checking
- Reservation management
- Order management
- Inventory management

## Project Structure

```text
CodeAlpha_RestaurantManagement/
│
├── restaurant/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── restaurantproject/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment:

```bash
venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run database migrations:

```bash
python manage.py migrate
```

7. Start the development server:

```bash
python manage.py runserver
```

8. Open the local development server:

```text
http://127.0.0.1:8000/
```

## Database
SQLite is used to store restaurant menu, table, reservation, order, and inventory information.

## Conclusion
This project demonstrates backend development using Django REST Framework, including REST APIs, database relationships, reservation management, order processing, and automatic inventory management.