#!/usr/bin/env python3

import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher

def encrypt(file_type, key, algorithm):

            salt = os.urandom(64)

            kdf = PBKDF2HMAC(
                    algorithm=SHA256(),
                    length=32,
                    salt=salt,
                    iterations=1000000,
                    backend=default_backend(),
            )

            key_derive = key.derive(key.encode())

            iv = os.urandom(16)
            Cipher = Cipher(algorithm)

