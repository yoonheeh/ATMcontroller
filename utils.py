import hashlib

def encrypt(password):
    encoded_password = password.encode()
    hashed_password = hashlib.sha256(encoded_password).hexdigest()
    return hashed_password