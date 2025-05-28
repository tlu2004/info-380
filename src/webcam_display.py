import cv2
import os
from datetime import datetime
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class WebcamFeed(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.setPixmap(QPixmap.fromImage(img))

    def save_current_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Create captures folder if it doesn't exist
            os.makedirs("captures", exist_ok=True)

            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captures/snapshot_{timestamp}.jpg"

            # Save image
            cv2.imwrite(filename, frame)
            print(f"📸 Saved: {filename}")

    def close(self):
        self.cap.release()