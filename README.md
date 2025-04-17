## hashlib module in Python

- generate secure hash values (also known as message digests) from data like strings or files.
- sha256() – Secure and commonly used.

## Example

import hashlib
data = "hello world"
hash_object = hashlib.sha256(data.encode())
hex_dig = hash_object.hexdigest()

print(hex_dig)
🔎 Output: A long SHA-256 hash string like
a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b...

## ✅ Why we use .encode():

- The hashlib functions like sha256() expect a byte object, not a string.
- data.encode() converts a string (like "hello") into bytes (like b'hello').

**if you try to pass a plain string, you’ll get a TypeError**

- hash_obj = hashlib.sha256(data)
- TypeError: Strings must be encoded before hashing

## ✅ Why we use .hexdigest():

- After you hash something, you get a binary digest — not very readable.
- .hexdigest() converts that binary digest into a readable hexadecimal string.

- 🟡 .digest() → raw bytes
- 🟢 .hexdigest() → hex string (what you usually want to print, compare, store, etc.)

- .encode() → turns your text into bytes ✅
- sha256() → hashes those bytes 🔐
- .hexdigest() → gives you a nice hex string 🧾

#### 🧠 When you hash data using hashlib.sha256, you get a result — but it’s not something you can easily read.

- There are two ways to look at the result:
- Bytes (raw format) — like weird unreadable computer stuff
- Hex string (readable format) — like normal letters and numbers

- If .digest() is the messy version,
- .hexdigest() is the clean, pretty version you actually want to use.

## ✅ 1. from cryptography.fernet import Fernet

- This line imports the Fernet **class** from the cryptography _library_.
- Fernet provides **symmetric encryption** (same key to encrypt and decrypt).
- It handles **AES encryption, key generation, signing, and timestamp**s, so you don’t have to.

## 🔑 2. KEY = Fernet.generate_key()

- This creates a new encryption key.
- The key is a random 32-byte base64-encoded string.
- You need this key to:
- Encrypt data
- Later decrypt that same data

**🛑 Important: If you lose this key, you can't decrypt the data — ever. You should store it securely (e.g., in an .env file, a config file, or a key vault).**

## 🔁 1. What is Symmetric Encryption?

- 🗝️ One key does both jobs: lock and unlock
- Imagine a padlock that uses the same key to lock and unlock.
  **You use the same key to:**
- Encrypt (lock) the message
- Decrypt (unlock) the message

### 🔐 Example:

- You encrypt a message with a key:
  **hello → [ENCRYPTED STUFF]**

- Later, you decrypt it with the same key:
  **[ENCRYPTED STUFF] → hello**

**This is called symmetric encryption, because it's the same (symmetrical) key for both actions.**

## ⚡ 2. What is AES Encryption?

**🧠 AES stands for Advanced Encryption Standard**

- It’s one of the most _trusted and widely used encryption_ methods in the world.

**_📦 In simple terms:_**

- AES turns your message into **super-scrambled data**
- Only someone with the correct key can unscramble it
  It's **fast and secure**, and that's why Fernet uses it under the hood

💡 You don’t have to write AES code yourself — Fernet handles it for you automatically.

## 🕒 3. What are Timestamps in Fernet?

- Fernet adds a timestamp to **every encrypted message**.

### Why?

- To know when the message was encrypted
- So you can set an expiration time

**🧠 In one sentence:**

- Fernet is a tool that lets you **securely lock data** with **one key (symmetric)** using AES, and it even tags it with a **timestamp** so you know how fresh the data is.

**st.session_state** is a **special dictionary** that lets you store data across user interactions — like **remembering values between button clicks or page refreshes**.
