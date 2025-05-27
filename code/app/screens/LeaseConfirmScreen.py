from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class LeaseConfirmScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lease Confirmed")
        layout = QVBoxLayout(self)
        label = QLabel("Lease was successful!")
        label.setStyleSheet("font-size: 18px; color: #228B22;")
        label.setWordWrap(True)
        layout.addWidget(label)
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)