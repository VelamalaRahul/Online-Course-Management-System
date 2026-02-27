import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

users = User.objects.all()
print(f"Total Users: {len(users)}")
print("-" * 50)

for u in users:
    print(f"Email:    {u.email}")
    print(f"Username: {u.username}")
    print(f"Active:   {u.is_active}")
    print(f"Is Staff: {u.is_staff}")
    print(f"Hashed:   {u.password.startswith('pbkdf2_sha256$')}")
    print(f"PW Start: {u.password[:20]}...")
    
    # Test common passwords if we suspect them
    for p in ['123', 'password123', 'admin', 'password']:
        if authenticate(username=u.email, password=p):
            print(f"  --> PASSWORD MATCH: {p}")
    print("-" * 50)

# Check USERNAME_FIELD
print(f"USERNAME_FIELD: {User.USERNAME_FIELD}")
print(f"REQUIRED_FIELDS: {User.REQUIRED_FIELDS}")