import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from accounts.models import User

# Reset main user
u1 = User.objects.filter(email='rachamadugujohith@gmail.com').first()
if u1:
    u1.set_password('password123')
    u1.save()
    print("Reset rachamadugujohith@gmail.com password to 'password123'")
else:
    # Create it if it doesn't exist for some reason
    User.objects.create_user(
        email='rachamadugujohith@gmail.com',
        username='rachamadugujohith',
        full_name='Rachamadugu Johith',
        password='password123'
    )
    print("Created rachamadugujohith@gmail.com with password 'password123'")

# Create second test user
u2, created = User.objects.get_or_create(
    email='finaltest@gmail.com',
    defaults={
        'username': 'finaltest',
        'full_name': 'Final Test',
        'role': 'Student'
    }
)
u2.set_password('finalpass123')
u2.save()
print("Created/Updated finaltest@gmail.com with password 'finalpass123'")