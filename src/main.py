import sys
from PyQt5.QtWidgets import QApplication, QWidget
from webcam_display import WebcamFeed
from ui_elements import InfoOverlay, AlertsOverlay
from PyQt5.QtWidgets import QPushButton


class MetaLensWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lookout Prototype")
        self.setGeometry(100, 100, 900, 500)
        self.setStyleSheet("background-color: black;")

        # Add webcam feed
        self.webcam = WebcamFeed(self)
        self.webcam.setGeometry(0, 0, 900, 500)

        # Add floating UI elements
        self.overlay = InfoOverlay(self)
        self.alerts = AlertsOverlay(self)
        
        # Inside MetaLensWindow.__init__:
        self.save_btn = QPushButton("📸 Save Photo", self)
        self.save_btn.setGeometry(20, 20, 120, 30)
        self.save_btn.clicked.connect(lambda: self.webcam.save_current_frame())
        self.save_btn.raise_()

    def closeEvent(self, event):
        self.webcam.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MetaLensWindow()
    window.show()
    sys.exit(app.exec_())
