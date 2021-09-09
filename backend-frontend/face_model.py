import cv2, os
import numpy as np
import tensorflow as tf
from flask import flash, redirect
from werkzeug.utils import secure_filename

EMOTIONS_merged = ["happy","angry", "sad", "neutral"]
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_files(request, upload_path):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    files = request.files.getlist('file')

    file_list = []

    for file in files:
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file_path = os.path.join(upload_path, secure_filename(file.filename))
            file.save(file_path)
            file_list.append(file_path)

    return file_list


def get_img_path(file_list):
    prop_list = np.array([0, 0, 0, 0])
    for img_path in file_list:
        prop_list = np.array([x + y for x, y in zip(prop_list, face_chk(img_path))])

    return prop_list.argmax()


def face_chk(img_path):
    # parameters for loading data and images
    detection_model_path = 'haarcascade_frontalface_default.xml'
    emotion_model_path = '_mini_XCEPTION.102-0.66.hdf5'

    face_detection = cv2.CascadeClassifier(detection_model_path)
    emotion_classifier = tf.keras.models.load_model(emotion_model_path, compile=False)
    EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

    img = cv2.imread(img_path, 0)
    faces = face_detection.detectMultiScale(img, scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(30, 30),
                                            flags=cv2.CASCADE_SCALE_IMAGE)

    if len(faces) > 0:
        faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = faces
        roi = img[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (64, 64))
        roi = roi.astype("float") / 255.0
        roi = tf.keras.preprocessing.image.img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        preds = emotion_classifier.predict(roi)[0]
        preds_merged = np.array([preds[0] + preds[2] + preds[5], preds[3] + preds[5], preds[1] + preds[4], preds[6]])

    return preds_merged


    # 모델 로드하기
    # from tf.keras.models import model_from_json
    # json_file = open("model.json", "r")
    # loaded_model_json = json_file.read()
    # json_file.close()
    # loaded_model = model_from_json(loaded_model_json)

    # 가중치 로드하기
    # loaded_model.load_weights("result/weight.h5")
