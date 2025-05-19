from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class CompletionScreen(QWidget):
    def __init__(self, user, data, photos, parent=None):
        super().__init__(parent)
        self.user = user
        self.data = data
        self.photos = photos

        self.setWindowTitle("Completion")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        label = QLabel("Completion Screen (Coming Soon)")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.setLayout(layout)
        self.showMaximized()