import cv2
import os
import numpy as np
import json

subjects = ['Elon Musk', 'Malala']


# Save subjects (authorized personnel) to a JSON file
def save_subjects(subjects, file_path=r'../Output Files/subjects.json'):
    with open(file_path, 'w') as f:
        json.dump(subjects, f)


# Load subjects (authorized personnel) from a JSON file
def load_subjects(file_path=r'../Output Files/subjects.json'):
    with open(file_path, 'r') as f:
        return json.load(f)


# Detect a face in the given image
def detectFace(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(r'../Input Files/lbpcascade_frontalface.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    if len(faces) == 0:
        return None, None

    (x, y, w, h) = faces[0]
    return gray[y:y + w, x:x + h]


# Initial training of the face recognition model with existing data
def initialTraining(data_folder_path=r'../Input Files/training-data'):
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []

    for dir_name in dirs:
        label = int(dir_name)
        subject_dir_path = data_folder_path + '/' + dir_name
        subject_images_names = os.listdir(subject_dir_path)

        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue

            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            face = detectFace(image)

            if face:
                faces.append(face)
                labels.append(label)

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(labels))
    face_recognizer.save(r'../Output Files/trained_face_recognizer.xml')

    save_subjects(subjects)

    return face_recognizer


# Train the model with new personnel data
def train(personnel_name, data_folder_path=r'../Input Files/training-data'):
    subjects.append(personnel_name)
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []

    for dir_name in dirs:
        label = int(dir_name)
        subject_dir_path = data_folder_path + '/' + dir_name
        subject_images_names = os.listdir(subject_dir_path)

        for image_name in subject_images_names:

            if image_name.startswith("."):
                continue

            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            face = detectFace(image)

            if face:
                faces.append(face)
                labels.append(label)

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(labels))
    face_recognizer.save(r'../Output Files/trained_face_recognizer.xml')

    save_subjects(subjects)

    return


# Predict the subject (authorized personnel) in the test image
def predict(model_path, test_img_path):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read(model_path)

    global subjects
    subjects = load_subjects()

    test_img = cv2.imread(test_img_path)
    img = test_img.copy()
    face = detectFace(img)

    try:
        label, confidence = face_recognizer.predict(face)
        label_text = subjects[label]
    except:
        return None

    return label_text

# initialTraining()
