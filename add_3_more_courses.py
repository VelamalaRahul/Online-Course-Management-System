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

# Create 3 new premium courses
new_courses = [
    {
        "title": "Advanced UI/UX Design Systems",
        "description": "Master the art of creating premium, scalable design systems using modern glassmorphism and motion principles.",
        "instructor_id": instructor,
        "category_id": category1,
        "price": 129,
        "level": "Advanced"
    },
    {
        "title": "Cybersecurity and Network Defense",
        "description": "Protect digital assets with advanced penetration testing, encryption systems, and threat intelligence.",
        "instructor_id": instructor,
        "category_id": category2,
        "price": 110,
        "level": "Intermediate"
    },
    {
        "title": "Cloud Native Architecture with AWS",
        "description": "Design high-availability systems using Kubernetes, AWS Lambda, and serverless architectures.",
        "instructor_id": instructor,
        "category_id": category1,
        "price": 159,
        "level": "Advanced"
    }
]

created_count = 0
for cd in new_courses:
    c, created = Course.objects.get_or_create(title=cd["title"], defaults=cd)
    if created:
        created_count += 1

print(f"Successfully created {created_count} NEW premium courses!")