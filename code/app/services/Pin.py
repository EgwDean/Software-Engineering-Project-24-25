from PyQt5.QtCore import QObject, pyqtSignal

class Pin(QObject):
    clicked = pyqtSignal()

    def __init__(self, latitude, longitude, title=""):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.title = title

    def on_click(self):
        self.clicked.emit()
