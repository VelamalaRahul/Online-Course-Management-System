import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from courses.models import Course, Lecture

def refresh():
    # Update Thumbnails
    courses = Course.objects.all()
    mapping = {
        'Web': '/media/thumbnails/web_dev.png',
        'Cyber': '/media/thumbnails/cybersecurity.png',
        'Cloud': '/media/thumbnails/cloud.png',
        'AI': '/media/thumbnails/ai_ml.png',
        'Machine': '/media/thumbnails/ai_ml.png',
        'Blockchain': '/media/thumbnails/blockchain.png',
        'DevOps': '/media/thumbnails/devops.png'
    }
    
    for c in courses:
        cat_name = c.category_id.name
        matched = False
        for key, val in mapping.items():
            if key.lower() in cat_name.lower() or key.lower() in c.title.lower():
                c.thumbnail_url = val
                matched = True
                break
        if not matched:
            c.thumbnail_url = '/media/thumbnails/web_dev.png' # Default
        c.save()
        print(f"Updated {c.title} with {c.thumbnail_url}")

    # Diversify Lectures
    lectures = Lecture.objects.all()
    types = ['video', 'video', 'lab', 'quiz', 'video']
    for i, l in enumerate(lectures):
        l.lecture_type = types[i % len(types)]
        if 'Quiz' in l.title: l.lecture_type = 'quiz'
        if 'Lab' in l.title: l.lecture_type = 'lab'
        l.save()
    print("Diversified lectures.")

if __name__ == "__main__":
    refresh()