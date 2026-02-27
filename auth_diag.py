import os
import django
from django.contrib.auth import authenticate

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from accounts.models import User

# Test existing users with a known password (if we can find one) or just create a test user
test_email = "diag_test@example.com"
test_pass = "diag_pass123"

# Cleanup if exists
User.objects.filter(email=test_email).delete()

# Create user via serializer (to mimic registration)
from accounts.serializers import UserSerializer
data = {
    "email": test_email,
    "username": "diag_test",
    "full_name": "Diag Test",
    "password": test_pass,
    "role": "student"
}
serializer = UserSerializer(data=data)
if serializer.is_valid():
    user = serializer.save()
    print(f"Created test user: {user.email}")
    
    # Try to authenticate using email as username
    auth_user = authenticate(username=test_email, password=test_pass)
    print(f"Auth with username={test_email}: {'SUCCESS' if auth_user else 'FAILED'}")
    
    # Try to authenticate using email explicitly
    auth_user_email = authenticate(email=test_email, password=test_pass)
    print(f"Auth with email={test_email}: {'SUCCESS' if auth_user_email else 'FAILED'}")
    
    # Check what SimpleJWT serializer sees
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    jwt_serializer = TokenObtainPairSerializer(data={"username": test_email, "password": test_pass})
    try:
        jwt_serializer.is_valid(raise_exception=True)
        print("SimpleJWT Serializer (username key): SUCCESS")
    except Exception as e:
        print(f"SimpleJWT Serializer (username key): FAILED - {jwt_serializer.errors}")

    # Test with email key
    jwt_serializer_email = TokenObtainPairSerializer(data={"email": test_email, "password": test_pass})
    try:
        jwt_serializer_email.is_valid(raise_exception=True)
        print("SimpleJWT Serializer (email key): SUCCESS")
    except Exception as e:
        print(f"SimpleJWT Serializer (email key): FAILED - {jwt_serializer_email.errors}")
else:
    print(f"Serializer errors: {serializer.errors}")

# Inspect existing users
print("\nExisting Users Check:")
for u in User.objects.all():
    print(f"Email: {u.email}, Username: {u.username}, Is Active: {u.is_active}, Password Hashed: {u.password.startswith('pbkdf2_sha256$')}")