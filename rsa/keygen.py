import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization




def iskey(keyname):
    return os.path.isdir("keys/"+keyname+"/")

def keygen(keyname):
    # private key gen
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    # public key gen
    public_key = private_key.public_key()

    # create keys directory
    if os.path.isdir("keys") == False :
        os.mkdir("keys",0o666)
    # create my key
    if iskey(keyname) == False :
        os.mkdir("keys/"+keyname+"/",0o666)

        # private key save
        serial_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open('keys/'+keyname+'/private_key.pem', 'wb') as f: f.write(serial_private)

        # public key save
        serial_pub = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open('keys/'+keyname+'/public_key.pem', 'wb') as f: f.write(serial_pub)
    else: print("Key existed")

def save_pub_key(key,keyname):
    # create keys directory
    if os.path.isdir("keys") == False :
        os.mkdir("keys",0o666)
    # create my key
    if iskey(keyname) == False :
        os.mkdir("keys/"+keyname+"/",0o666)
        # public key save
        serial_pub = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open('keys/'+keyname+'/public_key.pem', 'wb') as f: f.write(serial_pub)
    else:
        print('Key already existed.')

def save_pub_key_byte(key_byte,keyname):
    # create keys directory
    if os.path.isdir("keys") == False :
        os.mkdir("keys",0o666)
    # create my key
    if iskey(keyname) == False :
        os.mkdir("keys/"+keyname+"/",0o666)
        # public key save
        with open('keys/'+keyname+'/public_key.pem', 'wb') as f: f.write(key_byte)
    else:
        print('Key already existed.')
