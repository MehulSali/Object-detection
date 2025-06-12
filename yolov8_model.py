from ultralytics import YOLO
import pytesseract
import cv2

# Set your installed Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

model = YOLO('yolov8n.pt')  # You can use yolov8s.pt or other weights as well
CONF_THRESHOLD = 0.4

def detect_objects_and_text(frame):
    # Object Detection
    results = model(frame, verbose=False)
    object_labels = set()

    for r in results:
        for box in r.boxes:
            if float(box.conf[0]) >= CONF_THRESHOLD:
                cls = int(box.cls[0])
                object_labels.add(model.names[cls])

    # OCR - Optical Character Recognition
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray).strip()

    return list(object_labels), extracted_text
