import hashlib

data = "hello world"
hash_obj = hashlib.sha256(data.encode())
hex_dig = hash_obj.hexdigest()

print("hash obj:", hash_obj)
print("hex", hex_dig)


name = "sadaf"
hashed = hashlib.sha256(name.encode())

print("Raw Bytes: " , hashed.digest())
print("Readable Hex: " , hashed.hexdigest())
