from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class InvalidPaymentDetailsScreen(QDialog):
    def __init__(self, parent=None, reason=""):
        super().__init__(parent)
        self.setWindowTitle("Invalid Payment Details")
        self.setModal(True)
        layout = QVBoxLayout(self)

        # Show a more detailed message if a reason is provided
        if reason:
            message = f"The payment details you entered are invalid:\n\n{reason}\n\nPlease check your information and try again."
        else:
            message = "The payment details you entered are invalid.\nPlease check your information and try again."
        label = QLabel(message)
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