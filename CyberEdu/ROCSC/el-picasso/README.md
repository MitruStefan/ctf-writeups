# El Picasso Challenge Writeup

> **Category**: Rev\
> **Author**: Stefan

## TL;DR
Analyzing a 32-bit binary in IDA and finding a QR code from the graph view.

---

## Challenge Description
The challenge involves a binary that prints an ASCII cat. Our goal is to reverse engineer the binary to find the hidden flag.

## Solution

### Step 1: Checking the Binary
First, we use the `file` command to inspect the binary:

```sh
file el-picasso
```

The output indicates that it is a 32-bit dynamically linked binary, not stripped:

```
el-picasso: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, not stripped
```

Running the binary, it prints an ASCII cat:

<img src="https://i.imgur.com/RCGEbdh.png" alt="ASCII Cat" width="200"/>

### Step 2: Disassembling the Binary
Next, we disassemble the binary using Ghidra.

<img src="https://i.imgur.com/Gl4XONi.png" alt="Ghidra" width="500"/>

However, the output is mostly gibberish and the decompiler doesn't work. Switching to IDA Free, we get a more readable disassembly, but with a warning that the graph won't be shown because the limit is 1000.

<img src="https://i.imgur.com/Xre1tNQ.png" alt="IDA Free Warning" width="500"/>

### Step 3: Investigating the Disassembly
Upon further investigation, we find that the code is a mess. Googling `ctf vfmaddsub132ps` leads us to a presentation from [DEF CON 23](https://media.defcon.org/DEF%20CON%2023/DEF%20CON%2023%20presentations/DEF%20CON%2023%20-%20Chris-Domas-REpsych.pdf), which mentions that this instruction, among others, can be used to "psychologically torment" reverse engineers.

### Step 4: Decoding the QR Code
By changing the maximum graph limit in IDA Free, we reveal a graph that resembles a QR code.

<img src="https://i.imgur.com/rXZJu1l.png" alt="QR Code" width="300"/>

We screenshot the graph and adjust the colors in Photoshop to make it more visible.

<img src="https://i.imgur.com/qYWJjb6.png" alt="QR Code" width="300"/>

Scanning it reveals the flag.

<img src="https://i.imgur.com/D9cL5gV.png" alt="Flag" width="500"/>

## Flag
`ctf{1ff757b6b99229db80a208563aa98dfb5e4a592b34551ba44b63038c7bd442af}`