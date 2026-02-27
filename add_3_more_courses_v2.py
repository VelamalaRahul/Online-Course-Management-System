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

# Create 3 more premium courses
new_courses = [
    {
        "title": "Blockchain Enterprise Solutions",
        "description": "Architect decentralized applications and private blockchain networks for enterprise security and transparency.",
        "instructor_id": instructor,
        "category_id": category2,
        "price": 179,
        "level": "Advanced"
    },
    {
        "title": "Modern DevOps with Docker & Kubernetes",
        "description": "Scale applications globally using containerization, CI/CD pipelines, and automated orchestration.",
        "instructor_id": instructor,
        "category_id": category1,
        "price": 139,
        "level": "Intermediate"
    },
    {
        "title": "Emotional Intelligence for Leaders",
        "description": "Develop high-performance teams by mastering empathy, self-regulation, and strategic relationship management.",
        "instructor_id": instructor,
        "category_id": category2,
        "price": 95,
        "level": "Beginner"
    }
]

created_count = 0
for cd in new_courses:
    c, created = Course.objects.get_or_create(title=cd["title"], defaults=cd)
    if created:
        created_count += 1

print(f"Successfully created {created_count} MORE premium courses!")