import tkinter as tk
from tkinter import filedialog


# Function to select encryption or decryption
def selectEncryptOrDecrypt():
    def onEncryptClick():
        nonlocal choice
        choice = 'encrypt'
        dialog.destroy()

    def onDecryptClick():
        nonlocal choice
        choice = 'decrypt'
        dialog.destroy()

    def addAuthPersonnel():
        nonlocal choice
        choice = 'auth'
        dialog.destroy()

    choice = None

    dialog = tk.Tk()
    dialog.title("Select Encryption or Decryption")

    spelly_label = tk.Label(dialog, text='File/Folder Locker', font=('Arial', 20, 'bold'))
    spelly_label.pack()

    button_frame = tk.Frame(dialog)
    button_frame.pack()

    message = tk.Label(button_frame, text="Do you want to Encrypt or Decrypt?")
    message.pack(pady=10)

    encrypt_button = tk.Button(button_frame, text="Select Encrypt", command=onEncryptClick)
    encrypt_button.pack(side="left", padx=15, pady=15)

    decrypt_button = tk.Button(button_frame, text="Select Decrypt", command=onDecryptClick)
    decrypt_button.pack(side="right", padx=15, pady=15)

    auth_frame = tk.Frame(dialog)
    auth_frame.pack()

    add_auth_personnel_button = tk.Button(auth_frame, text="Add Auth Personnel", command=addAuthPersonnel)
    add_auth_personnel_button.pack(padx=10, pady=10)

    dialog.mainloop()

    return choice


# Function to select file or folder
def selectFileOrFolder():
    def onFileClick():
        nonlocal choice
        choice = 'file'
        dialog.destroy()

    def onFolderClick():
        nonlocal choice
        choice = 'folder'
        dialog.destroy()

    choice = None

    dialog = tk.Tk()
    dialog.title("Select File or Folder")

    message = tk.Label(dialog, text="Do you want to select a file or a folder?")
    message.pack(pady=10)

    file_button = tk.Button(dialog, text="Select File", command=onFileClick)
    file_button.pack(side="left", padx=10, pady=10)

    folder_button = tk.Button(dialog, text="Select Folder", command=onFolderClick)
    folder_button.pack(side="right", padx=10, pady=10)

    dialog.mainloop()

    if choice == 'file':
        file_or_folder = filedialog.askopenfilename()
    elif choice == 'folder':
        file_or_folder = filedialog.askdirectory()
    else:
        file_or_folder = None

    return file_or_folder


# Function to select an image
def selectImage():
    def onImgSelect():
        nonlocal image
        image = filedialog.askopenfilenames(
            title="Select an Images",
            filetypes=[("Image file", "*.jpg;*.jpeg")],
        )
        dialog.destroy()

    image = None

    dialog = tk.Tk()
    dialog.title("Select Image")

    message = tk.Label(dialog, text="Select an image of an authorized personnel")
    message.pack(pady=10)

    browse_button = tk.Button(dialog, text="Browse Image", command=onImgSelect)
    browse_button.pack(padx=10, pady=10)

    dialog.mainloop()

    return image


# Function to select multiple images for authentication
def selectAuthPersonnel():
    def onImgsSelect():
        nonlocal images
        images = filedialog.askopenfilenames(
            title="Select at least 5 Images",
            filetypes=[("Image files", "*.jpg;*.jpeg")],
        )
        dialog.destroy()

    images = None

    dialog = tk.Tk()
    dialog.title("Select Images")

    message = tk.Label(dialog, text="Select at least 5 images of the new authorized personnel")
    message.pack(pady=10)

    browse_button = tk.Button(dialog, text="Browse Images", command=onImgsSelect)
    browse_button.pack(padx=10, pady=10)

    dialog.mainloop()

    return images
