import os
import django
from django.contrib.auth import authenticate

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from accounts.models import User

with open('auth_results.txt', 'w') as f:
    users = User.objects.all()
    f.write(f"Total Users: {len(users)}\n")
    f.write("-" * 50 + "\n")
    
    for u in users:
        f.write(f"Email:    {u.email}\n")
        f.write(f"Username: {u.username}\n")
        f.write(f"Active:   {u.is_active}\n")
        
        # Test 1: authenticate(username=...)
        # We try 'password123' as it's a common test password used here
        res_un = authenticate(username=u.email, password='password123')
        f.write(f"Auth(username={u.email}, pw='password123'): {'SUCCESS' if res_un else 'FAIL'}\n")
        
        # Test 2: authenticate(email=...)
        res_em = authenticate(email=u.email, password='password123')
        f.write(f"Auth(email={u.email}, pw='password123'): {'SUCCESS' if res_em else 'FAIL'}\n")

        # Test with '123'
        res_un2 = authenticate(username=u.email, password='123')
        f.write(f"Auth(username={u.email}, pw='123'): {'SUCCESS' if res_un2 else 'FAIL'}\n")

        f.write("-" * 50 + "\n")

    f.write(f"USERNAME_FIELD: {User.USERNAME_FIELD}\n")