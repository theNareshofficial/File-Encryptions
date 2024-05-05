#!/usr/bin/env python3

import os
import argparse
import getpass          #  Hide the password
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Ansi color code
RED = '\033[31m'        # RED color
GREEN = '\033[32m'      # GREEN color
RESET = '\033[0m'       # RESET all color
BLINK = '\033[5m'       # Blink content

# Banner
banner = f"""{GREEN}{BLINK}

     +-----------+
     |  File.txt |
     +-----------+
           |
           V
   +------------------+
   |  Encryption Key  |
   +------------------+
           |
           V 
    +---------------+
    | Encrypted     |
    |  File.txt.enc |
    +---------------+
    {RESET}
            Author  : Naresh
            Github  : https://github.com/theNareshofficial
            Youtube : https://www.youtube.com/@nareshtechweb930

{RESET}{RED}
"""

print(banner)

def encrypt_file(file_path, algorithm, key):    # Encrypt function

    salt = os.urandom(16)  # Generate a random salt

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Key length for AES
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    derived_key = kdf.derive(key.encode())  # Derive the key from the password

    # AES-256 in CBC mode with a random IV
    iv = os.urandom(16)         # iv mean Initialization Vector
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Read and encrypt the file
    with open(file_path, 'rb') as f:
        plaintext = f.read()

    # Apply PKCS7 padding to ensure the plaintext is a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher_text = encryptor.update(padded_data) + encryptor.finalize()

    # Save the encrypted data to a new file with .enc extension
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, 'wb') as f:
        f.write(salt + iv + cipher_text)         # Store the salt and IV in the beginning of the file for later decryption

         # Enable for remove original file    
        #os.remove(file_path)        # remove original file

    print(f"File '{file_path}' encrypted successfully as '{encrypted_file_path}'")


def decrypt_file(file_path, key):  # Decrypt function

    # Read the encrypted data
    with open(file_path, 'rb') as f:
        salt = f.read(16)  # Extract the salt
        iv = f.read(16)  # Extract the IV
        cipher_text = f.read()  # The rest is cipher text

    # Derive the key from the password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )

    # If the password is incorrect, an exception will be thrown
    try:
        derived_key = kdf.derive(key.encode())
    except Exception as e:
        print("Incorrect password.")
        pass
    except KeyboardInterrupt:
        pass

    cipher = Cipher(algorithms.AES(derived_key),
                    modes.CBC(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the cipher_text and remove padding
    padded_data = decryptor.update(cipher_text) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()

    print("File decrypted successfully. Here is the content:")
    print(plaintext.decode('utf-8'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        "Encrypt or Decrypt a file with a specified algorithm and key.")
    parser.add_argument("--file",
                        type=str,
                        required=True,
                        help="Path to the file to encrypt or decrypt.")
    parser.add_argument("--mode",
                        choices=["encrypt", "decrypt"],
                        required=True,
                        help="Whether to encrypt or decrypt.")
    parser.add_argument("--algorithm",
                        type=str,
                        default="AES",
                        help="Encryption algorithm to use. Default is AES.")

    args = parser.parse_args()

    # Get the secret key (password) from the user
    key = getpass.getpass("Enter your password: ")

    if args.algorithm != "AES":
        print("Currently, only AES encryption is supported.")
        exit(1)

    if args.mode == "encrypt":
        encrypt_file(args.file, args.algorithm, key)
    elif args.mode == "decrypt":
        decrypt_file(args.file, key)
