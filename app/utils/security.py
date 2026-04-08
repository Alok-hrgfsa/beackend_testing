import bcrypt

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    plain_bytes = plain.encode("utf-8")[:72]
    return bcrypt.checkpw(plain_bytes, hashed.encode("utf-8"))