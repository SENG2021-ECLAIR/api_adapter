from hashlib import md5
from uuid import uuid4


def generate_token() -> str:
    return str(uuid4())


def encrypt_password(password):
    return md5(password.encode()).hexdigest()
