import cv2, os
import numpy as np
from PIL import Image

from sfk.settings import MEDIA_ROOT
from sfr.models import Face, Classifier


def test_rec(user, face):
    clf = Classifier.objects.get(user=user)
    recognizer = cv2.face.EigenFaceRecognizer_create()
    recognizer.read(MEDIA_ROOT + '/' + str(clf.recognizer))
    width_d, height_d = 280, 280

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = Image.open(face.img).convert('L')
    image = np.array(gray, 'uint8')
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        id_pred, conf = recognizer.predict(cv2.resize(image[y: y + h, x: x + w], (width_d, height_d)))

    name_pred = Face.objects.get(pk=id_pred).name
    return name_pred


def get_images(user, face_cascade):
    faces = Face.objects.filter(user=user)
    width_d, height_d = 280, 280
    images = []
    labels = []
    for face in faces:
        gray = Image.open(face.img).convert('L')
        image = np.array(gray, 'uint8')
        subject_name = face.id
        faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            images.append(cv2.resize(image[y: y + h, x: x + w], (width_d, height_d)))
            labels.append(subject_name)
    return images, labels


def overfitting_rec(user):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    recognizer = cv2.face.EigenFaceRecognizer_create()
    images, labels = get_images(user, face_cascade)
    recognizer.train(images, np.array(labels))
    recognizer.save(MEDIA_ROOT + "/recognizers/" + str(user.id) + ".yml")
    cleaned_data = {}
    if not Classifier.objects.filter(user=user).exists():
        cleaned_data['user'] = user
        cleaned_data['recognizer'] = "recognizers/" + str(user.id) + ".yml"
        Classifier.objects.create(**cleaned_data)


