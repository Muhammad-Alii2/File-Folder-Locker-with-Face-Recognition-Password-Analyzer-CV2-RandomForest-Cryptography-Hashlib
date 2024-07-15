from cryptography.fernet import Fernet
import os


# Generate a new key for encryption
def generateKey():
    return Fernet.generate_key()


# Save the generated key to a file
def saveKey(key, key_path):
    with open(key_path, 'wb') as key_file:
        key_file.write(key)


# Load the encryption key from a file
def loadKey(key_path):
    with open(key_path, 'rb') as key_file:
        return key_file.read()


# Encrypt a file using the provided key
def encryptFile(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)


# Encrypt all files in a folder using the provided key
def encryptFolder(folder_path, key):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encryptFile(file_path, key)


# Decrypt a file using the provided key
def decryptFile(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)


# Decrypt all files in a folder using the provided key
def decryptFolder(folder_path, key):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            decryptFile(file_path, key)
