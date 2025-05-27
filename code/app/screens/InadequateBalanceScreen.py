from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class InadequateBalanceScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Inadequate Balance")
        self.setModal(True)
        layout = QVBoxLayout(self)
        label = QLabel("Your balance is not sufficient to complete this purchase.\nPlease top up your account and try again.")
        label.setStyleSheet("font-size: 16px; color: #b22222;")
        label.setWordWrap(True)
        layout.addWidget(label)
        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a3f54;
                color: white;
                padding: 8px 24px;
                border-radius: 6px;
                font-size: 15px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #4682b4;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)