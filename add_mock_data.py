import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from courses.models import Course, Category
from reviews.models import Review
from accounts.models import User

# Ensure we have a category
category, _ = Category.objects.get_or_create(name="Web Development", defaults={"slug": "web-development"})
category2, _ = Category.objects.get_or_create(name="Data Science", defaults={"slug": "data-science"})

# Ensure we have an instructor user
instructor, _ = User.objects.get_or_create(
    email="instructor@example.com", 
    defaults={"username": "instructor@example.com", "full_name": "Jane Instructor", "role": "instructor"}
)
# Set password safely just in case
if instructor.password == "":
    instructor.set_password("password123")
    instructor.save()

# Ensure we have a student user for reviews
student, _ = User.objects.get_or_create(
    email="student@example.com", 
    defaults={"username": "student@example.com", "full_name": "Bob Student", "role": "student"}
)

# Create 3 courses
course1, c1_created = Course.objects.get_or_create(
    title="Advanced UI Design Patterns",
    defaults={
        "description": "Master modern UI/UX design with practical examples.",
        "instructor_id": instructor,
        "category_id": category,
        "price": 49,
        "level": "Advanced"
    }
)

course2, c2_created = Course.objects.get_or_create(
    title="Django REST Framework Pro",
    defaults={
        "description": "Build scalable APIs with Django REST Framework.",
        "instructor_id": instructor,
        "category_id": category,
        "price": 59,
        "level": "Intermediate"
    }
)

course3, c3_created = Course.objects.get_or_create(
    title="Machine Learning Foundations",
    defaults={
        "description": "Understand core concepts of ML and data prediction models.",
        "instructor_id": instructor,
        "category_id": category2,
        "price": 79,
        "level": "Beginner"
    }
)

if c1_created or c2_created or c3_created:
    print("Successfully created 3 mock courses!")
else:
    print("Mock courses already existed in the database.")

# Add some reviews
from reviews.models import Review

Review.objects.get_or_create(
    course_id=course1,
    student_id=student,
    defaults={"rating": 5, "comment": "Amazing course!"}
)

Review.objects.get_or_create(
    course_id=course2,
    student_id=student,
    defaults={"rating": 4, "comment": "Great content."}
)

print("Mock reviews added successfully.")