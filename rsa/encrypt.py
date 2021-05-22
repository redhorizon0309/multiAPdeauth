from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def encrypt_msg(public_key,msg):
    cyphertext = public_key.encrypt(
        plaintext=msg.encode('utf-8'),
        padding=padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA512(),
                    label=None
                )
    )
    return cyphertext