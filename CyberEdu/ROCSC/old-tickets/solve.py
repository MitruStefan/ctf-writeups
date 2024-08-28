import requests
from hashlib import md5
import re

url = "http://34.107.71.117:31882"
timestamp = 1628168161

for i in range(1000000):
    code = md5(str(timestamp + i).encode('utf-8')).hexdigest()
    data = {"code": code}
    r = requests.post(url, data=data)

    pattern = r'ctf\{[0-9a-fA-F]{64}\}'
    match = re.search(pattern, r.text)
    if match:
        print(timestamp + i)
        print(match.group())
        break
