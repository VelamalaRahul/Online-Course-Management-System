import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from courses.models import Lecture

lectures = Lecture.objects.all()
for lecture in lectures:
    lecture.video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    lecture.save()

print("Updated all video URLs to a working MP4 sample.")