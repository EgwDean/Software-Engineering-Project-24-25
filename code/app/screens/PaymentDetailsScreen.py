import re
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from screens.InvalidPaymentDetailsScreen import InvalidPaymentDetailsScreen
from screens.ConfirmSubscriptionScreen import ConfirmSubscriptionScreen
from screens.InadequateBalanceScreen import InadequateBalanceScreen
from services.ManageBalanceClass import ManageBalanceClass
import services.Database as DB
from datetime import date

class PaymentDetailsScreen(QDialog):
    def __init__(self, user, selected_package, payment_method, parent=None):
        super().__init__(parent)
        self.user = user
        self.selected_package = selected_package
        self.payment_method = payment_method

        self.setWindowTitle("Payment Details")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Enter details for: {payment_method}"))

        self.card_number = QLineEdit()
        self.card_number.setPlaceholderText("Card Number" if payment_method == "Credit Card" else "Account/Email")
        layout.addWidget(self.card_number)

        self.cvv = None
        self.expiry = None
        if payment_method == "Credit Card":
            self.expiry = QLineEdit()
            self.expiry.setPlaceholderText("Expiry Date (MM/YY)")
            layout.addWidget(self.expiry)
            self.cvv = QLineEdit()
            self.cvv.setPlaceholderText("CVV")
            layout.addWidget(self.cvv)

        self.confirm_btn = QPushButton("Confirm Payment")
        self.confirm_btn.clicked.connect(self.enterDetails)
        layout.addWidget(self.confirm_btn)

    def checkDetails(self):
        """
        Checks the validity of the payment details.
        Returns (invalid: bool, reason: str)
        """
        reason = ""
        invalid = False
        if self.payment_method == "Credit Card":
            card_number = self.card_number.text().strip()
            expiry = self.expiry.text().strip() if self.expiry else ""
            cvv = self.cvv.text().strip() if self.cvv else ""

            if not re.fullmatch(r"\d{13,19}", card_number):
                invalid = True
                reason = "Card number must be 13-19 digits."
            elif not re.fullmatch(r"(0[1-9]|1[0-2])\/\d{2}", expiry):
                invalid = True
                reason = "Expiry date must be in MM/YY format."
            elif not re.fullmatch(r"\d{3,4}", cvv):
                invalid = True
                reason = "CVV must be 3 or 4 digits."
        else:
            if not self.card_number.text().strip():
                invalid = True
                reason = "Please enter your account/email."
        return invalid, reason

    def displayNotEnough(self, reason):
        dlg = InvalidPaymentDetailsScreen(self, reason=reason)
        dlg.exec_()

    def displayConfirm(self):
        confirm_screen = ConfirmSubscriptionScreen(self.user, self.selected_package)
        confirm_screen.exec_()
        if self.parent():
            self.parent().close()  # Close SubPackagesScreen if this dialog was opened from it
        from screens.MySubscriptionsScreen import MySubscriptionsScreen
        self.close()  # Close PaymentDetailsScreen itself
        self.sub_screen = MySubscriptionsScreen(self.user)
        self.sub_screen.show()

    def enterDetails(self):
        invalid, reason = self.checkDetails()
        if invalid:
            self.displayNotEnough(reason)
            return

        ok, msg = ManageBalanceClass.checkBalance(self.user, self.selected_package)
        if ok:
            self.displayConfirm()
        else:
            dlg = InadequateBalanceScreen(self)
            dlg.exec_()