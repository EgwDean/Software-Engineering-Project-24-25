from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QButtonGroup

class SelectPaymentMethodScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Payment Method")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Choose a payment method:"))

        self.button_group = QButtonGroup(self)
        self.methods = ["Credit Card", "PayPal", "Bank Transfer"]
        for method in self.methods:
            btn = QPushButton(method)
            btn.setCheckable(True)
            self.button_group.addButton(btn)
            layout.addWidget(btn)

        confirm_btn = QPushButton("Confirm")
        confirm_btn.clicked.connect(self.accept)
        layout.addWidget(confirm_btn)

    def chooseMethod(self):
        checked = self.button_group.checkedButton()
        return checked.text() if checked else None