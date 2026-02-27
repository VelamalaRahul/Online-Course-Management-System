import os
import django
from django.contrib.auth import authenticate

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from accounts.models import User

# Try to find a user we know (e.g., sri@gmail.com which was 123)
email = 'sri@gmail.com'
password = '123'

user_obj = User.objects.filter(email=email).first()
if not user_obj:
    print(f"User {email} not found in DB.")
else:
    print(f"User {email} found. ID: {user_obj.pk}, Active: {user_obj.is_active}")
    print(f"Password in DB: {user_obj.password[:30]}...")
    
    # Test 1: authenticate(username=email, password=password)
    res1 = authenticate(username=email, password=password)
    print(f"Auth(username=email): {'SUCCESS' if res1 else 'FAIL'}")
    
    # Test 2: authenticate(email=email, password=password)
    res2 = authenticate(email=email, password=password)
    print(f"Auth(email=email): {'SUCCESS' if res2 else 'FAIL'}")
    
    # Test 3: Check password manually
    from django.contrib.auth.hashers import check_password
    res3 = check_password(password, user_obj.password)
    print(f"check_password manually: {'SUCCESS' if res3 else 'FAIL'}")

# Also test the 'diag_test@example.com' user
email_diag = 'diag_test@example.com'
pass_diag = 'diag_pass123'
user_diag = User.objects.filter(email=email_diag).first()
if user_diag:
    print(f"\nUser {email_diag} found. Auth(username=...): {'SUCCESS' if authenticate(username=email_diag, password=pass_diag) else 'FAIL'}")