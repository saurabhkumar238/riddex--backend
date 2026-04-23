from passlib.context import CryptContext
from jose import jwt

SECRET = "secret123"

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_token(username):
    return jwt.encode({"user": username}, SECRET, algorithm="HS256")