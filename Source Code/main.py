from gui import selectEncryptOrDecrypt, selectFileOrFolder, selectImage, selectAuthPersonnel
from encryption import generateKey, saveKey, loadKey, encryptFile, encryptFolder, decryptFile, decryptFolder
from hashing import hashPassword, saveHashedPassword, loadHashedPassword
from face_recognition import train, predict
from password_analyzer import predictPasswordStrength
import os
import shutil
import joblib
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")


# Utility function to extract the name from the given path
def getName(path):
    base_name = os.path.basename(path)
    name, _ = os.path.splitext(base_name)
    return name

# Select the operation to perform (Encrypt, Decrypt, or Authenticate)
choice = selectEncryptOrDecrypt()

if choice == 'encrypt':
    file_folder = selectFileOrFolder()

    if file_folder:
        loaded_model = joblib.load(r'../Output Files/password_strength_model.pkl')
        password = ''
        while True:
            password = input("Set a password: ")
            strength = predictPasswordStrength(password, loaded_model)
            if strength == 0:
                print("Password strength low, please enter a new password")
                continue
            if strength == 1:
                user_input = input("Password strength medium, do u wanna continue? y/n: ")
                if user_input == 'y':
                    break
                else:
                    continue
            if strength == 2:
                print("Password strength strong, you can continue with your encryption")
                break
        hashed_password = hashPassword(password)
        saveHashedPassword(hashed_password, fr'../Output Files/{getName(file_folder)}pass.txt')
        key = generateKey()
        saveKey(key, fr'../Output Files/{getName(file_folder)}.key')
        if os.path.isfile(file_folder):
            encryptFile(file_folder, key)
        else:
            encryptFolder(file_folder, key)

        print("File/Folder encrypted")

    else:
        print('No file selected.')

elif choice == 'decrypt':
    file_folder = selectFileOrFolder()

    if file_folder:
        hashed_password = loadHashedPassword(fr'../Output Files/{getName(file_folder)}pass.txt')
        key = loadKey(fr'../Output Files/{getName(file_folder)}.key')

        while True:
            input_password = input("Enter password to unlock: ")

            if hashPassword(input_password) == hashed_password:
                break
            else:
                print("Incorrect password!")

        while True:
            image_path = selectImage()
            if image_path:
                prediction = predict(r'../Output Files/trained_face_recognizer.xml', image_path[0])

                if prediction:

                    if os.path.isfile(file_folder):
                        decryptFile(file_folder, key)
                    else:
                        decryptFolder(file_folder, key)
                    print('Hello ' + prediction + ', File/Folder decrypted.')
                    os.remove(fr'../Output Files/{getName(file_folder)}.key')
                    os.remove(fr'../ Output Files/{getName(file_folder)}pass.txt')
                    break

                else:
                    print("Not authorized. Try again!")

            else:
                print('No image selected.')
                break

    else:
        print('No file selected.')

elif choice == 'auth':
    while True:
        image_paths = selectAuthPersonnel()
        if len(image_paths) >= 5:
            break
        else:
            print('Select at least 5 images please.')

    try:
        existing_folders = [int(name) for name in os.listdir(r'../Input Files/training-data') if
                            os.path.isdir(os.path.join(r'../Input Files/training-data', name))]
        next_folder_number = max(existing_folders, default=0) + 1
        new_folder_path = os.path.join(r'../Input Files/training-data', str(next_folder_number))

        os.makedirs(new_folder_path)

        for image_path in image_paths:
            shutil.copy(image_path, new_folder_path)

        new_auth_personnel = input('Enter new auth personnel name: ')

        result = train(new_auth_personnel)
        print(result)
        if result:
            print('New auth personnel ' + new_auth_personnel + ' added')
        else:
            os.rmdir(new_folder_path)

    except Exception as e:
        try:
            shutil.rmtree(new_folder_path)
        except OSError as e:
            print(f"Error: {e}")
        print('Issue detecting the face, try again with different pictures')
