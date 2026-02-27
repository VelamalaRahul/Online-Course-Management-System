import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from courses.models import Course, Category
from accounts.models import User

# Grab existing category and instructor
category1 = Category.objects.filter(slug="web-development").first()
category2 = Category.objects.filter(slug="data-science").first()
instructor = User.objects.filter(role="instructor").first()

if not instructor:
    instructor, _ = User.objects.get_or_create(
        email="instructor2@example.com", 
        defaults={"username": "instructor2@example.com", "full_name": "Pro Instructor", "role": "instructor"}
    )

# Create 4 new courses
new_courses = [
    {
        "title": "Full-Stack Web Development Bootcamp",
        "description": "Learn frontend to backend development using React and Django.",
        "instructor_id": instructor,
        "category_id": category1,
        "price": 99,
        "level": "Beginner"
    },
    {
        "title": "Data Engineering Fundamentals",
        "description": "Master data pipelines, ETL processes, and big data architecture.",
        "instructor_id": instructor,
        "category_id": category2,
        "price": 89,
        "level": "Intermediate"
    },
    {
        "title": "Advanced Python Architecture",
        "description": "Design secure, scalable, and maintainable Python applications.",
        "instructor_id": instructor,
        "category_id": category1,
        "price": 120,
        "level": "Advanced"
    },
    {
        "title": "AI and Deep Learning with PyTorch",
        "description": "Build state-of-the-art neural networks for real-world applications.",
        "instructor_id": instructor,
        "category_id": category2,
        "price": 149,
        "level": "Advanced"
    }
]

created_count = 0
for cd in new_courses:
    c, created = Course.objects.get_or_create(title=cd["title"], defaults=cd)
    if created:
        created_count += 1

print(f"Successfully created {created_count} NEW mock courses!")