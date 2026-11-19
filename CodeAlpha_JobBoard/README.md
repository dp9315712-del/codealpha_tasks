# Job Board Platform

## Project Overview
The Job Board Platform is a backend application developed using Python, Django, and Django REST Framework. It allows employers to post jobs and candidates to upload resumes, apply for jobs, and track their applications.

## Technologies Used
- Python
- Django
- Django REST Framework
- SQLite

## Features
- Employer and candidate management
- Create job listings
- Search and view job listings
- Upload candidate resumes in PDF format
- Resume file size validation (maximum 5 MB)
- Apply for available jobs
- Track job applications
- Update application status
- Automatically create employer notifications
- Manage data through Django Admin

## Database Models
- Employer
- JobListing
- Candidate
- Resume
- JobApplication
- EmployerNotification

## API Functionality
The project provides REST API endpoints for:
- Posting jobs
- Searching jobs
- Uploading resumes
- Applying for jobs
- Tracking applications
- Updating application status

## Project Structure

```text
CodeAlpha_JobBoard/
│
├── jobs/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── jobboardproject/
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

## Database
SQLite is used to store employer, candidate, job listing, resume, application, and notification information.

## Conclusion
This project demonstrates backend development using Django REST Framework, including job management, resume uploads, job applications, application tracking, and employer notifications.
