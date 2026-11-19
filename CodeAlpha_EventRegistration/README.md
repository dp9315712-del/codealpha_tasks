# Event Registration System

## Project Overview
The Event Registration System is a backend application developed using Python and Django REST Framework. It allows users to view events, register for events, check their registrations, and cancel registrations.

## Technologies Used
- Python
- Django
- Django REST Framework
- SQLite

## Features
- View all available events
- View event details
- User authentication for registration
- Register for an event
- Prevent duplicate registrations
- Check available seats
- Automatically decrease available seats after registration
- View personal registrations
- Cancel event registration
- Automatically restore seats after cancellation

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/events/` | Get all events |
| GET | `/api/events/<id>/` | Get event details |
| POST | `/api/events/<id>/register/` | Register for an event |
| GET | `/api/my-registrations/` | View my registrations |
| DELETE | `/api/registrations/<id>/cancel/` | Cancel registration |

## Project Structure

```text
CodeAlpha_EventRegistration/
│
├── eventproject/
├── events/
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

6. Run migrations:

```bash
python manage.py migrate
```

7. Start the development server:

```bash
python manage.py runserver
```

8. Open in your browser:

```text
http://127.0.0.1:8000/
```

## Database
SQLite is used to store event and registration information.

## Conclusion
This project demonstrates backend development using Django REST Framework, including REST APIs, authentication, database relationships, and event seat management.
