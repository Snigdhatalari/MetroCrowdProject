import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_people():

    cap = cv2.VideoCapture(0)  # webcam

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return 0

    results = model(frame)

    count = 0

    for r in results:
        for box in r.boxes:
            if int(box.cls) == 0 and float(box.conf) > 0.5:
                count += 1

    return count