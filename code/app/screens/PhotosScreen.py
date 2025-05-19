from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class PhotosScreen(QWidget):
    def __init__(self, user, data, parent=None):
        super().__init__(parent)
        self.user = user
        self.data = data  # Dictionary with the form fields

        self.setWindowTitle("Upload Photos")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        label = QLabel("Photos Screen (Coming Soon)")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.setLayout(layout)