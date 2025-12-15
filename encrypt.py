from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Load public key
with open("keys/public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(
        f.read(),
        backend=default_backend()
    )

# Generate AES key
aes_key = os.urandom(32)  # AES-256
iv = os.urandom(16)

# Read original file
with open("sample.txt", "rb") as f:
    data = f.read()

# Encrypt file using AES
cipher = Cipher(
    algorithms.AES(aes_key),
    modes.CFB(iv),
    backend=default_backend()
)
encryptor = cipher.encryptor()
encrypted_data = encryptor.update(data) + encryptor.finalize()

# Save encrypted file
with open("encrypted.bin", "wb") as f:
    f.write(iv + encrypted_data)

# Encrypt AES key using RSA public key
encrypted_key = public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open("encrypted_key.bin", "wb") as f:
    f.write(encrypted_key)

print("File encrypted successfully")
