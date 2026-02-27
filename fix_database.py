import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocms.settings')
django.setup()

from accounts.models import User

print("--- Data Remediation ---")
for u in User.objects.all():
    changed = False
    
    # Lowercase email
    if u.email != u.email.lower():
        print(f"Normalizing email: {u.email} -> {u.email.lower()}")
        u.email = u.email.lower()
        changed = True
        
    # Check for plain text passwords (dangerous!)
    # If the password doesn't contain a '$' (Django's standard) 
    # and is long enough to be a password but not a hash
    if not u.password.startswith('pbkdf2_sha256$') and not u.password.startswith('bcrypt'):
        print(f"WARNING: Plain text password detected for {u.email}. Re-hashing it.")
        u.set_password(u.password)
        changed = True
        
    if changed:
        u.save()
        print(f"Fixed user: {u.email}")
    else:
        print(f"User OK: {u.email}")

print("\nRemediation complete.")