from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class ConfirmSubscriptionScreen(QDialog):
    def __init__(self, user, package, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Subscription Confirmed")
        layout = QVBoxLayout(self)
        label = QLabel(f"Subscription to '{package['plan']}' was successful!\nThank you, {user.username}.")
        label.setStyleSheet("font-size: 18px; color: #228B22;")
        label.setWordWrap(True)
        layout.addWidget(label)

        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)