from hashlib import sha256


def hash_gsrn(data):
    x = str(data).encode()

    for i in range(1000):
        x = sha256(x).digest()

    return x.hex()
