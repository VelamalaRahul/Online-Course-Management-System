import urllib.request
import urllib.error
import json
import time

email = f"newuser_{int(time.time())}@example.com"
password = "newpassword123"

print("Registering:", email)
reg_data = json.dumps({
    "username": email,
    "email": email,
    "full_name": "New User",
    "password": password,
    "role": "student"
}).encode('utf-8')

req1 = urllib.request.Request('http://127.0.0.1:8000/api/register/', data=reg_data, headers={'Content-Type': 'application/json'})
try:
    reg_resp = urllib.request.urlopen(req1)
    print("Register Status:", reg_resp.getcode())
    print("Register Body:", reg_resp.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("Register Status:", e.code)
    print("Register Body:", e.read().decode('utf-8'))

print("\nLogging in:", email)
log_data = json.dumps({
    "email": email,
    "password": password
}).encode('utf-8')

req2 = urllib.request.Request('http://127.0.0.1:8000/api/token/', data=log_data, headers={'Content-Type': 'application/json', 'Origin': 'null'})
try:
    log_resp = urllib.request.urlopen(req2)
    print("Login Status:", log_resp.getcode())
    print("Login Body:", log_resp.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("Login Status:", e.code)
    if e.code == 500:
        print("500 HTML saved")
        with open('error_500_new.html', 'w', encoding='utf-8') as f:
            f.write(e.read().decode('utf-8'))
    else:
        print("Login Body:", e.read().decode('utf-8'))
except Exception as e:
    print("Other error:", e)