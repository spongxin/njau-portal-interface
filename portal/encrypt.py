from Crypto.Cipher import AES
from base64 import b64encode
import random
import string


def encrypt(password, key) -> str:
    """AES.CBC 算法加密"""
    key = key.encode("utf-8")
    iv = randomstring().encode("utf-8")
    encryptor = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    encrypted = encryptor.encrypt(pkcs7padding(randomstring(64) + password).encode("utf-8"))
    return b64encode(encrypted).decode()


def pkcs7padding(text, bs=16) -> str:
    """pkcs7 填充算法"""
    padding = bs - len(text.encode("utf-8")) % bs
    return text + chr(padding) * padding


def randomstring(size=16) -> str:
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
