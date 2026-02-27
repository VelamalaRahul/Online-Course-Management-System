import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from courses.models import Course, Category
from accounts.models import User

# Grab existing category and instructor
category1, _ = Category.objects.get_or_create(name="AI & Machine Learning", defaults={"slug": "ai-ml"})
category2, _ = Category.objects.get_or_create(name="Cybersecurity", defaults={"slug": "cybersecurity"})
category3, _ = Category.objects.get_or_create(name="Web & Cloud", defaults={"slug": "web-cloud"})

instructor = User.objects.filter(role="instructor").first()

if not instructor:
    instructor, _ = User.objects.get_or_create(
        email="commander@genesis.io", 
        defaults={"username": "commander", "full_name": "Ghost-in-Command", "role": "instructor"}
    )

# Create 4 new premium sci-fi themed courses
new_courses = [
    {
        "title": "Quantum Algorithm Synthesis",
        "description": "Construct high-dimensional logic across quantum architectures. A masterclass in breaking classical processing limits.",
        "instructor_id": instructor,
        "category_id": category1,
        "price": 299,
        "level": "Advanced"
    },
    {
        "title": "Neural Shield Configuration",
        "description": "Deploy immutable firewall grids and counter-intrusive protocols against zero-day orbital threats.",
        "instructor_id": instructor,
        "category_id": category2,
        "price": 185,
        "level": "Intermediate"
    },
    {
        "title": "Planetary Node Infrastructure",
        "description": "Build asynchronous edge-computing microservices spanning multiple orbital relays using AWS and Rust.",
        "instructor_id": instructor,
        "category_id": category3,
        "price": 249,
        "level": "Advanced"
    },
    {
        "title": "Holographic Interface Design",
        "description": "Pioneer immersive, low-latency UI frameworks designed for mixed-reality spatial computing environments.",
        "instructor_id": instructor,
        "category_id": category3,
        "price": 95,
        "level": "Beginner"
    }
]

created_count = 0
for cd in new_courses:
    c, created = Course.objects.get_or_create(title=cd["title"], defaults=cd)
    if created:
        created_count += 1
        print(f"Created: {c.title}")

print(f"\\nSuccessfully created {created_count} NEW premium courses!")
