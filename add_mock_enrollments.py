import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from courses.models import Course, Module, Lecture
from accounts.models import User
from enrollments.models import Enrollment, LectureProgress

# Get our test user
user = User.objects.filter(email='johi@gmail.com').first()
if not user:
    print("Test user 'johi@gmail.com' not found. Creating one...")
    user, _ = User.objects.get_or_create(
        email='johi@gmail.com',
        username='johi@gmail.com',
        full_name='Test User Johi'
    )
    user.set_password('password123')
    user.save()

# Get some courses
courses = list(Course.objects.all()[:2])
if not courses:
    print("No courses available to enroll in.")
    exit()

print(f"Creating enrollments for {user.email}...")

for course in courses:
    enrollment, created = Enrollment.objects.get_or_create(
        student_id=user,
        course_id=course,
        defaults={'status': 'active'}
    )
    
    if created:
        print(f"Enrolled in {course.title}")
    
    # Get modules and lectures for this course
    modules = Module.objects.filter(course_id=course)
    
    # We will simulate 50% completion
    total_lectures = 0
    completed_lectures = 0
    
    for mod in modules:
        lectures = Lecture.objects.filter(module_id=mod)
        for i, lecture in enumerate(lectures):
            total_lectures += 1
            is_completed = (total_lectures % 2 == 0) # mark every other lecture
            
            ProgressObj, p_created = LectureProgress.objects.get_or_create(
                enrollment_id=enrollment,
                lecture_id=lecture,
                defaults={
                    'completed': is_completed,
                    'completed_at': timezone.now() if is_completed else None
                }
            )
            
            if is_completed and p_created:
                completed_lectures += 1

print("Successfully injected mock enrollments and progress!")