# Online Course Management System (OCMS) Blueprint

## Project Overview
The Online Course Management System (OCMS) is a Django-based web application designed for managing online courses, user accounts, enrollments, and reviews. It provides a RESTful API built with Django Rest Framework (DRF) and uses PostgreSQL as its primary database and Redis for caching.

## Project Structure

### Core Configuration (`ocms/ocms/`)
- `settings.py`: Contains project-wide settings, including database configuration (PostgreSQL), installed apps, middleware, and caching settings (Redis).
- `urls.py`: The root URL configuration, routing requests to individual application URLs.
- `wsgi.py` & `asgi.py`: Entry points for WSGI and ASGI compatible web servers.

### Applications

#### 1. Accounts (`accounts/`)
Handles user identity and authentication.
- `models.py`: Defines the custom `User` model with fields like `email`, `password`, `full_name`, and `role`.
- `views.py`: API endpoints for listing and managing user details.
- `serializers.py`: Handles serialization of `User` objects for the API.
- `urls.py`: Routes for user-related API endpoints.

#### 2. Courses (`courses/`)
The core module for managing course content.
- `models.py`: Defines the hierarchy of course content: `Category` -> `Course` -> `Module` -> `Lecture`.
- `views.py`: CRUD operations for categories, courses, modules, and lectures.
- `serializers.py`: Serializers for all course-related models.
- `urls.py`: Routes for course management.

#### 3. Enrollments (`enrollments/`)
Manages student registrations and their progress in courses.
- `models.py`: Defines `Enrollment` (links students to courses) and `LectureProgress` (tracks completion of individual lectures).
- `views.py`: API endpoints for managing enrollments and tracking progress.
- `serializers.py`: Serializers for enrollment and progress data.

#### 4. Reviews (`reviews/`)
Enables students to provide feedback on courses.
- `models.py`: Defines the `Review` model with `rating` and `comment` fields.
- `views.py`: API endpoints for submitting and viewing course reviews.
- `serializers.py`: Serializer for course reviews.

#### 5. Dashboard (`dashboard/`)
Provides analytical data for the system.
- `views.py`: Contains the `analytics` view which aggregates system-wide statistics like total users, courses, and enrollments.
- `urls.py`: Route for the analytics dashboard.

### Frontend (`frontend/`)
The user-facing layer of the application, served directly by Django.
- `index.html`: The main dashboard and landing page with dynamic analytics.
- `login.html`: Premium authentication interface.
- `courses.html`: Course discovery grid with filtering.
- `course_detail.html`: Immersive learning environment for course content.
- `profile.html`: Student dashboard and progress tracker.
- `styles.css`: Centralized design system using HSL colors, glassmorphism, and Outfit typography.

## Technical Architecture

### 1. API Architecture
The project follows a standard RESTful pattern using Django Rest Framework (DRF):
- **Endpoints**: Most entities support standard CRUD via Function Based Views (FBVs) with `@api_view`.
- **Serialization**: `ModelSerializer` is used across all apps for consistent JSON formatting.
- **Pagination**: `PageNumberPagination` is configured globally with a default page size of 2 (seen in `accounts` and `courses` views).

### 2. Caching Strategy
- **Redis Integration**: High-frequency endpoints (user lists, course lists, etc.) are cached using Redis.
- **Duration**: The `@cache_page(100)` decorator is applied to views to optimize performance and reduce database load.

### 3. Frontend-Backend Integration
- **Template System**: Django's `TemplateView` is used to serve `index.html`, `login.html`, and other frontend pages.
- **Static Files**: The `frontend` directory is configured as both a template source and a static file source (`STATICFILES_DIRS`).
- **Dynamic Content**: Frontend components (like the analytics dashboard) interact with the backend via asynchronous `fetch()` calls to the API endpoints (e.g., `/analytics/`).

### 4. Authentication & Security
- **JWT**: Secure authentication is handled via `rest_framework_simplejwt`.
- **Permissions**: `IsAuthenticated` check is enforced on core API views.

## Key Technologies
- **Backend Framework**: Django
- **API Framework**: Django Rest Framework (DRF)
- **Database**: PostgreSQL
- **Caching**: Redis (via `django_redis`)
- **Authentication**: JWT (SimpleJWT)
- **Filtering**: Django-filter
- **Frontend Design**: Vanilla CSS (Glassmorphism), Google Fonts (Outfit)

---

## How to Run This Project Locally

### 1. Prerequisites
- **Python 3.10+**
- **PostgreSQL**: Ensure a database named `ocms_db` is created.
- **Redis**: Should be running on port `6380`.

### 2. Environment Setup
Create and activate a virtual environment:
```powershell
python -m venv env
.\env\Scripts\activate
```

### 3. Install Dependencies
```powershell
pip install django djangorestframework django-filter django-redis psycopg2-binary djangorestframework-simplejwt
```

### 4. Database Migrations
Apply the database schema:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Running the Application
Start the development server:
```powershell
python manage.py runserver
```
The application will be accessible at `http://127.0.0.1:8000/`.

### 6. Accessing Frontend
- **Landing Page**: `http://127.0.0.1:8000/`
- **Course Library**: `http://127.0.0.1:8000/courses/`
- **User Profile**: `http://127.0.0.1:8000/profile/`
- **Admin Portal**: `http://127.0.0.1:8000/admin/` (requires creating a superuser via `python manage.py createsuperuser`)