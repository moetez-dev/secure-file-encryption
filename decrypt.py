from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Load private key
with open("keys/private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend()
    )

# Load encrypted AES key
with open("encrypted_key.bin", "rb") as f:
    encrypted_key = f.read()

# Decrypt AES key
aes_key = private_key.decrypt(
    encrypted_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Load encrypted file
with open("encrypted.bin", "rb") as f:
    iv = f.read(16)
    encrypted_data = f.read()

# Decrypt file using AES
cipher = Cipher(
    algorithms.AES(aes_key),
    modes.CFB(iv),
    backend=default_backend()
)
decryptor = cipher.decryptor()
decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

# Save decrypted file
with open("decrypted.txt", "wb") as f:
    f.write(decrypted_data)

print("File decrypted successfully")
