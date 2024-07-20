from flask import Flask, request, jsonify
import cv2 as cv
import numpy as np

app = Flask(__name__)

# Load models
faceProto = "modelNweight/opencv_face_detector.pbtxt"
faceModel = "modelNweight/opencv_face_detector_uint8.pb"
genderProto = "modelNweight/gender_deploy.prototxt"
genderModel = "modelNweight/gender_net.caffemodel"

genderList = ['Male', 'Female']

faceNet = cv.dnn.readNet(faceModel, faceProto)
genderNet = cv.dnn.readNet(genderModel, genderProto)
padding = 20

def getFaceBox(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)
    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
    return frameOpencvDnn, bboxes

def detect_gender(frame):
    frameFace, bboxes = getFaceBox(faceNet, frame)
    genders = []
    for bbox in bboxes:
        face = frame[max(0, bbox[1] - padding):min(bbox[3] + padding, frame.shape[0] - 1),
                     max(0, bbox[0] - padding):min(bbox[2] + padding, frame.shape[1] - 1)]

        blob = cv.dnn.blobFromImage(face, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        genders.append(gender)
    return genders

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    in_memory_file = file.read()
    np_img = np.frombuffer(in_memory_file, np.uint8)
    img = cv.imdecode(np_img, cv.IMREAD_COLOR)

    if img is None:
        return jsonify({'error': 'Invalid image'}), 400

    genders = detect_gender(img)
    return jsonify({'genders': genders})

if __name__ == "__main__":
    app.run(debug=True)
