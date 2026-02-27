import os
import django
from django.contrib.auth import authenticate

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from accounts.models import User

print("--- User Data Audit ---")
users = User.objects.all()
for u in users:
    is_hashed = u.password.startswith("pbkdf2_sha256$") or u.password.startswith("bcrypt")
    print(f"ID: {u.pk}")
    print(f"  Email: {u.email}")
    print(f"  Username: {u.username}")
    print(f"  Active: {u.is_active}")
    print(f"  Hashed: {is_hashed}")
    print(f"  PW Start: {u.password[:15]}...")
    print("-" * 20)

print("\n--- Model natural keys ---")
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    print(f"USERNAME_FIELD: {User.USERNAME_FIELD}")
    print(f"REQUIRED_FIELDS: {User.REQUIRED_FIELDS}")
except Exception as e:
    print(f"Error checking model: {e}")