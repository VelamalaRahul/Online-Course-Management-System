import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from courses.models import Course, Module, Lecture

# Fetch all existing courses
courses = Course.objects.all()

if not courses:
    print("No courses found. Please run add_mock_data.py and add_more_courses.py first.")
    exit()

# Sample working YouTube videos (creative commons / tutorial placeholders)
sample_videos = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ", # Placeholder classic
    "https://www.youtube.com/watch?v=1bvwjXPEJzY", # Relaxing 
    "https://www.youtube.com/watch?v=jNQXAC9IVRw", # Me at the zoo
    "https://www.youtube.com/watch?v=2b1zKeouKgo", # LoFi
]

print(f"Adding modules, lectures, and videos to {len(courses)} courses...")

for course in courses:
    # Check if this course already has modules
    if Module.objects.filter(course_id=course).exists():
        print(f"Course '{course.title}' already has modules. Skipping.")
        continue
        
    print(f"Processing course: {course.title}")
    
    # Create Module 1
    mod1 = Module.objects.create(
        course_id=course,
        title="Introduction & Setup",
        order=1
    )
    
    # Add lectures to Module 1
    Lecture.objects.create(
        module_id=mod1,
        title="Welcome to the Course",
        video_url=random.choice(sample_videos),
        notes="Welcome to the beginning of your journey.",
        order=1,
        duration=5
    )
    Lecture.objects.create(
        module_id=mod1,
        title="Environment Setup",
        video_url=random.choice(sample_videos),
        notes="Install required tools and dependencies.",
        order=2,
        duration=12
    )

    # Create Module 2
    mod2 = Module.objects.create(
        course_id=course,
        title="Core Concepts",
        order=2
    )
    
    # Add lectures to Module 2
    Lecture.objects.create(
        module_id=mod2,
        title="Understanding the Architecture",
        video_url=random.choice(sample_videos),
        notes="Breaking down the components.",
        order=1,
        duration=20
    )
    Lecture.objects.create(
        module_id=mod2,
        title="Building Your First Feature",
        video_url=random.choice(sample_videos),
        notes="Hands on practical application.",
        order=2,
        duration=35
    )
    Lecture.objects.create(
        module_id=mod2,
        title="Summary and Next Steps",
        video_url=random.choice(sample_videos),
        notes="Wrapping up what we learned.",
        order=3,
        duration=8
    )

print("Successfully injected modules, lectures, and video URLs into all courses!")