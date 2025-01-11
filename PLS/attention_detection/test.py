import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Webcam not accessible!")
else:
    print("Webcam initialized successfully!")
cap.release()