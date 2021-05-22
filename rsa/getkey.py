from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def to_text(value, encoding="utf-8"):
    if not value:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode(encoding)
    return str(value)

def to_binary(value, encoding="utf-8"):
    if not value:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode(encoding)
    return to_text(value).encode(encoding)

def get_private_key (keyname):
    filepath = 'keys/'+keyname+'/private_key.pem'
    with open(filepath, "rb") as key_file:
        pem = to_binary(key_file.read())
        private_key = serialization.load_pem_private_key(
            pem,
            password=None,
            backend=default_backend()
        )
    return private_key
                  
def get_public_key (keyname):
    filepath = 'keys/'+keyname+'/public_key.pem'
    with open(filepath, "rb") as key_file:
        pem = to_binary(key_file.read())
        public_key = serialization.load_pem_public_key(
            pem,
            backend=default_backend()
        )
    return public_key