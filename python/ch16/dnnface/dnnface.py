import numpy as np
import cv2 as cv


model = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = 'deploy.prototxt'
#model = 'opencv_face_detector_uint8.pb'
#config = 'opencv_face_detector.pbtxt'

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print('Camera open failed!')
    exit()

net = cv.dnn.readNet(model, config)

if net.empty():
    print('Net open failed!')
    exit()

while True:
    _, frame = cap.read()
    if frame is None:
        break

    blob = cv.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
    net.setInput(blob)
    detect = net.forward()

    (h, w) = frame.shape[:2]
    detect = detect[0, 0, :, :]

    for i in range(detect.shape[0]):
        confidence = detect[i, 2]
        if confidence < 0.5:
            break

        x1 = int(detect[i, 3] * w)
        y1 = int(detect[i, 4] * h)
        x2 = int(detect[i, 5] * w)
        y2 = int(detect[i, 6] * h)

        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))

        label = 'Face: %4.3f' % confidence
        cv.putText(frame, label, (x1, y1 - 1), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv.LINE_AA)

    cv.imshow('frame', frame)

    if cv.waitKey(1) == 27:
        break

cv.destroyAllWindows()