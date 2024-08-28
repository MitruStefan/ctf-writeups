# old-tickets Challenge Writeup

> **Category**: Web\
> **Author**: Stefan

## TL;DR
Bruteforce timestamps to find the correct ticket hash and retrieve the flag.

---

## Challenge Description
Accessing the website, we have a simple ticket system. We can input a name and message and submit a ticket, but nothing will happen.

## Solution

### Step 1: Analyzing the Source Code

To begin, I inspected the source code of the website for any hidden clues and I discovered a comment embedded in the HTML:

```html
<!-- Our first bug was: d63af914bd1b6210c358e145d61a8abc. Please fix now! -->
```

This hash is something that could be useful later in the challenge.

### Step 2: Intercepting and Examining Requests

When I submitted a ticket, I noticed the server made a `GET` request instead of the typical `POST` or `PUT`. This was unusual behavior for submitting form data.

To further investigate, I used Burp Suite to send an `OPTIONS` request to the server, revealing that the server also supports `PUT` and `POST` methods.

<img src="https://i.imgur.com/w4cVAVA.png" alt="Request Image" width="100%"/>

### Step 3: Sending a POST Request

Next, I crafted a `POST` request using Burp Suite. Upon sending this request, the server returned `500 Internal Server Error`. Analyzing the error response, it exposed a traceback with useful information about the server's code.

<img src="https://i.imgur.com/8QniUPt.png" alt="Code Image" width="500"/>

### Step 4: Adding a Code Parameter

Following the hints from the error message, I added a `code` parameter to the `POST` request. After doing so, the server responded successfully, but nothing appeared to change visually on the website. Using the hash `d63af914bd1b6210c358e145d61a8abc` found earlier as the `code` value resulted in the server telling us to `Try harder!`.

<img src="https://i.imgur.com/u2YT2mM.png" alt="Response Image" width="600"/>

### Step 5: Identifying the Hash Type

I used the hash-identifier tool and it indicated that the hash was most likely an MD5 hash.

<img src="https://i.imgur.com/TXoIbee.png" alt="Hash Image" width="400"/>

### Step 6: Decrypting the Hash

I then navigated to [hashes.com](https://hashes.com/en/decrypt/hash) and used the hash. The result was an integer, which appeared to be a timestamp.

<img src="https://i.imgur.com/T7CFvUy.png" alt="Hash Result Image" width="300"/>

### Step 7: Formulating a Bruteforce Strategy

Realizing that the hash was a timestamp and recalling the server's message to `Try harder!` I deduced that the server required a specific timestamp to generate the correct ticket hash and reveal the flag. This led us to develop a bruteforce strategy: incrementally adjust the timestamp, hash it, and send it to the server until I find the correct one.

### Step 8: Writing and Running the Script

With a plan in place, I wrote a Python script to automate the bruteforce process. The script computes the MD5 hash of incremented timestamps and sends them in `POST` requests to the server until it retrieves the correct flag.

> **Note**: During bruteforcing, I also encountered a response containing `ctf{Try harder!}`, which required me to adjust the script to continue searching until it finds the actual flag, not just any string that starts with `ctf{`.

<img src="https://i.imgur.com/AvwU5kv.png" alt="Try harderImage" width="300"/>

### Step 9: Obtaining the Flag

After running the script, it successfully identified the correct timestamp and retrieved the flag from the server.

## Script
```python
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
```

## Flag

```
ctf{4086d9012b250dc1d821340f23b4af9b29d780552434175cb713b6d7502885c9}
```