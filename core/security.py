from passlib.context import CryptContext


password_context = CryptContext(schemes="bcrypt")


def hash_password(password: str):
    new_pass = password_context.hash(password)
    return new_pass


def verify_password(old_password: str, new_password: str):
    return password_context.verify(old_password, new_password)
