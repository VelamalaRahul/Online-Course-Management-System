import urllib.request
import urllib.error
import json

data = json.dumps({"email":"rachamadugujohith@gmail.com","password":"password123"}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/api/token/', data=data, headers={'Content-Type': 'application/json', 'Origin': 'null'})

try:
    resp = urllib.request.urlopen(req)
    print('Success:', resp.read())
except urllib.error.HTTPError as e:
    print('Error code:', e.code)
    html = e.read().decode('utf-8')
    with open('error_500.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Saved error_500.html')
except Exception as e:
    print('Other error:', e)