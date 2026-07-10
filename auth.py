import bcrypt

def hash_password(password: str):
    # Convert string to bytes, generate salt, and hash
    password_bytes = password.encode('utf-8')
    # Bcrypt limits input to 72 bytes
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes[:72], salt)
    return hashed.decode('utf-8')

def verify_password(plain_password, hashed_password):
    # Convert inputs to bytes and check
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes[:72], hashed_bytes)