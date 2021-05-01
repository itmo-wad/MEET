from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def check_password(password, db_hash):
    hash = sha256(password.encode()).hexdigest()
    return hash == db_hash
