import cv2
import easyocr
import numpy as np
import re
from collections import Counter
import warnings

# ──────────────────────────────────────────────
# Suppress irrelevant warnings
warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────
# EasyOCR Reader (CPU)
reader = easyocr.Reader(['en'], gpu=False)

# ──────────────────────────────────────────────
# Plate Smoother for flicker-free display
class PlateSmoother:
    def __init__(self, window=5):
        self.history = []
        self.window = window

    def update(self, plate):
        if plate:
            self.history.append(plate)
            if len(self.history) > self.window:
                self.history.pop(0)

    def get_best(self):
        if not self.history:
            return None
        return Counter(self.history).most_common(1)[0][0]

smoother = PlateSmoother(window=5)

# ──────────────────────────────────────────────
# Drawing helpers
def draw_plate(frame, bbox, text):
    x, y, w, h = bbox
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    label = f"PLATE: {text}"
    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
    cv2.rectangle(frame, (x, y - th - 10), (x + tw + 6, y), (0, 255, 0), -1)
    cv2.putText(frame, label, (x + 3, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

def draw_status(frame, text, color=(0,255,0)):
    cv2.rectangle(frame, (10,5), (400,40), (0,0,0), -1)
    cv2.putText(frame, text, (20,32), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

# ──────────────────────────────────────────────
# Video capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    plates_detected = False
    best_plate_text = None

    # Preprocess frame for contour detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(blur, 30, 200)

    # Find contours
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if len(approx) == 4:  # rectangle candidate
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            if 2 <= aspect_ratio <= 6 and w > 60 and h > 15:
                # Crop ROI
                roi = gray[y:y+h, x:x+w]

                # EasyOCR
                ocr_results = reader.readtext(roi)
                plate_text = ''
                for _, t, _ in ocr_results:
                    plate_text += t

                if plate_text:
                    # Uppercase + alphanumeric only
                    plate_text = ''.join(filter(str.isalnum, plate_text.upper()))

                    # Optional: Indian number plate regex filter
                    match = re.search(r'[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{4}', plate_text)
                    if match:
                        plate_text = match.group()
                        smoother.update(plate_text)
                        best_plate_text = smoother.get_best()
                        draw_plate(frame, (x, y, w, h), best_plate_text)
                        draw_status(frame, "NUMBER PLATE DETECTED", (0,255,0))
                        plates_detected = True
                        break

    if not plates_detected and best_plate_text:
        # Show last stable plate
        draw_status(frame, f"LAST PLATE: {best_plate_text}", (0,200,255))
    elif not plates_detected:
        draw_status(frame, "Scanning...", (0,0,255))

    cv2.imshow("ALPR CPU", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
