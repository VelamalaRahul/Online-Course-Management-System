🚀 Online Course Management System (OCMS)

The Online Course Management System (OCMS) is a full-stack web application developed with Django and Django REST Framework to streamline the process of managing and consuming online courses. The platform enables users to securely create accounts, explore course offerings, enroll in learning programs, monitor their progress, and share feedback through a structured review system. The application follows a modular Django architecture and exposes well-organized REST APIs that support seamless frontend integration.

🌟 Key Features

Secure Authentication – JWT-based user registration and login

Course Catalog – Organized course and category management

Enrollment Tracking – Students can enroll and monitor progress

Review System – Authenticated users can rate and review courses

Personal Dashboard – Snapshot of user learning activity

REST API Support – Clean, scalable API endpoints

Responsive Frontend – Built with HTML, CSS, and JavaScript

Performance Ready – Optional Redis caching for faster responses

🧰 Technology Stack

Backend

Django

Django REST Framework

Simple JWT

django-filter

Database

SQLite (default)

PostgreSQL (production ready)

Caching

Redis via django-redis (optional)

Frontend

HTML

CSS

JavaScript

📁 Repository Layout
ocms/
│
├── accounts/        # User model and authentication logic
├── courses/         # Course and category APIs
├── enrollments/     # Enrollment workflows
├── reviews/         # Ratings and feedback
├── dashboard/       # User statistics
├── frontend/        # Templates and static assets
├── ocms/            # Core project configuration
└── manage.py
⚙️ Local Setup Guide
✅ Requirements

Python 3.10 or newer

Redis (optional)

PostgreSQL (optional)

1. Clone the project
git clone https: https://github.com/VelamalaRahul/Online-Course-Management-System
2. Create and activate virtual environment
python -m venv env

Windows

env\Scripts\activate

macOS/Linux

source env/bin/activate
3. Install dependencies
pip install django djangorestframework django-filter django-redis psycopg2-binary djangorestframework-simplejwt
4. Run migrations
python manage.py makemigrations
python manage.py migrate
5. Create admin user
python manage.py createsuperuser
6. Start the server
python manage.py runserver

Visit: http://127.0.0.1:8000/

🔐 Authentication Endpoints

POST /api/token/ → generate access token

POST /api/token/refresh/ → refresh token


🌐 Main Routes
/ – Home

/login/ – User login

/register/ – User registration

/courses/ – Course listing

/profile/ – User profile

/reviews/ – Course reviews
/admin/ – Django admin

🧩 Design Overview

The system is built around a REST-first architecture where Django REST Framework handles data operations and Django templates render the user interface. Core APIs are protected using JWT authentication, and frequently accessed endpoints can be cached using Redis to improve response times. The modular app structure makes the project easy to extend and maintain.

🔮 Possible Enhancements

Payment integration for paid courses

Email verification workflow

Role-based permissions (admin/instructor/student)

Video lecture streaming

Docker containerization

React or Next.js frontend

👤 Maintainer

Rahul Velamala

📜 Usage License

This project is intended for academic learning and portfolio demonstration.
