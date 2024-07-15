import hashlib


# Hash a password using SHA-256
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Save the hashed password to a file
def saveHashedPassword(hashed_password, file_path):
    with open(file_path, 'w') as file:
        file.write(hashed_password)


# Load the hashed password from a file
def loadHashedPassword(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None
