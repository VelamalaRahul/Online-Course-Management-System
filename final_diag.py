import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from accounts.models import User

# List all users and their hashing status
print("--- Current User State ---")
for u in User.objects.all():
    is_hashed = u.password.startswith("pbkdf2_sha256$")
    print(f"Email: {u.email}, Hashed: {is_hashed}, Password Sample: {u.password[:20]}...")

# Optimization: If the user knows their password, they can re-register.
# But I will try to fix the test account if it was created incorrectly.
test_user = User.objects.filter(email='diag_test@example.com').first()
if test_user:
    print(f"\nVerifying test user {test_user.email}...")
    from django.contrib.auth import authenticate
    auth = authenticate(username=test_user.email, password="diag_pass123")
    print(f"Auth result: {'SUCCESS' if auth else 'FAILED'}")