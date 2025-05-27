from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox

class CancelSubScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Cancellation")
        layout = QVBoxLayout()
        label = QLabel("Are you sure you want to cancel your subscription?")
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        yes_btn = QPushButton("Yes, Cancel")
        no_btn = QPushButton("No")
        button_layout.addWidget(yes_btn)
        button_layout.addWidget(no_btn)
        layout.addLayout(button_layout)

        yes_btn.clicked.connect(lambda: self.done(QMessageBox.Yes))
        no_btn.clicked.connect(lambda: self.done(QMessageBox.No))

        self.setLayout(layout)