import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from accounts.models import User

users = User.objects.all()
print(f"Total users: {len(users)}")
for u in users:
    is_hashed = u.password.startswith("pbkdf2_sha256$") or u.password.startswith("bcrypt")
    print(f"Email: {u.email}, Username: {u.username}, Has hashed password: {is_hashed}")