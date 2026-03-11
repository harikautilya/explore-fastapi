import hashlib
import base64
async def encrpty_string(string: str):
    encoded_string =string.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(encoded_string)
    binary_hash = hash_object.digest() 
    base64_string = base64.b64encode(binary_hash).decode('utf-8')
    return base64_string
