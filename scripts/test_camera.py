import cv2
print("OpenCV version:", cv2.__version__)
try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit(1)
    ret, frame = cap.read()
    if ret:
        print("Camera OK")
    else:
        print("Error: Could not read frame.")
    cap.release()
except Exception as e:
    print("Error:", e)
