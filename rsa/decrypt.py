from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_msg(private_key,cyphertext):
    cleartext = private_key.decrypt(
        ciphertext=cyphertext,
        padding=padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA512(),
                    label=None
                )
    )
    return cleartext