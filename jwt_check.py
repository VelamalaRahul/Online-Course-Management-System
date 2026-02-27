import os
import django
from rest_framework import serializers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

print("--- SimpleJWT Key Check ---")
print(f"Serializer fields: {list(TokenObtainPairSerializer().fields.keys())}")

# Test with 'username' key
data_un = {"username": "test@test.com", "password": "pass"}
s_un = TokenObtainPairSerializer(data=data_un)
print(f"Valid with 'username' key: {s_un.is_valid()}")
if not s_un.is_valid():
    print(f"  Errors: {s_un.errors}")

# Test with 'email' key
data_em = {"email": "test@test.com", "password": "pass"}
s_em = TokenObtainPairSerializer(data=data_em)
print(f"Valid with 'email' key: {s_em.is_valid()}")
if not s_em.is_valid():
    print(f"  Errors: {s_em.errors}")