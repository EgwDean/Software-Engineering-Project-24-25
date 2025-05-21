from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QPushButton, QMessageBox, QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt
import services.Database as DB
from services.ManageSubsClass import ManageSubsClass
from screens.PaymentMethodScreen import PaymentMethodScreen
from screens.PaymentDetailsScreen import PaymentDetailsScreen

class SubPackagesScreen(QWidget):
    def __init__(self, user=None, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Subscription Packages")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.showMaximized()

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.main_layout)

        # Add the back button at the top
        back_button = QPushButton("Back To Map")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #2a3f54;
                color: white;
                padding: 10px 0;
                border-radius: 6px;
                font-size: 15px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4682b4;
            }
        """)
        back_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        back_button.clicked.connect(self.go_back_to_map)
        self.main_layout.addWidget(back_button)

        # Use ManageSubsClass for subscription check
        if ManageSubsClass.has_active_subscription(self.user.username):
            self.show_my_subscriptions()
        else:
            self.show_subscription_packages()

    def go_back_to_map(self):
        self.close()

    def show_subscription_packages(self):
        # Remove all widgets except the back button (assumed at index 0)
        while self.main_layout.count() > 1:
            widget = self.main_layout.itemAt(1).widget()
            if widget:
                widget.setParent(None)

        # Fetch plans from the database
        db = DB.Database()
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM subscription")
        plans = cursor.fetchall()
        cursor.close()
        conn.close()

        # Layout for cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        cards_layout = QHBoxLayout(container)
        cards_layout.setSpacing(30)

        for plan in plans:
            card = QFrame()
            card.setMinimumWidth(280)
            card.setMaximumWidth(320)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            card.setStyleSheet("""
                QFrame {
                    background: #f8fbff;
                    border-radius: 16px;
                    border: 2px solid #87ceeb;
                    padding: 18px 18px 18px 18px;
                    margin: 10px;
                }
                QFrame:hover {
                    border: 2.5px solid #4682b4;
                    background: #e6f2fa;
                }
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(10)
            card_layout.setContentsMargins(8, 8, 8, 8)

            plan_label = QLabel(plan["plan"])
            plan_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2a3f54;")
            plan_label.setAlignment(Qt.AlignCenter)
            plan_label.setWordWrap(True)

            price_label = QLabel(f"Price: €{plan['price']}")
            price_label.setStyleSheet("font-size: 16px; color: #28a745;")
            price_label.setAlignment(Qt.AlignCenter)
            price_label.setWordWrap(True)

            commission_label = QLabel(f"Commission: {plan['commission']}%")
            commission_label.setStyleSheet("font-size: 14px; color: #555;")
            commission_label.setAlignment(Qt.AlignCenter)
            commission_label.setWordWrap(True)

            select_btn = QPushButton("Select")
            select_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a3f54;
                    color: white;
                    padding: 10px 0;
                    border-radius: 6px;
                    font-size: 15px;
                    margin-top: 10px;
                }
                QPushButton:hover {
                    background-color: #4682b4;
                }
            """)
            select_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            select_btn.clicked.connect(lambda _, p=plan: self.on_package_selected(p))

            card_layout.addWidget(plan_label)
            card_layout.addWidget(price_label)
            card_layout.addWidget(commission_label)
            card_layout.addStretch()
            card_layout.addWidget(select_btn)

            cards_layout.addWidget(card)

        container.setLayout(cards_layout)
        scroll.setWidget(container)
        scroll.setMinimumHeight(350)
        self.main_layout.addWidget(scroll)

    def on_package_selected(self, package):
        self.selected_package = package
        dlg = PaymentMethodScreen(self)
        if dlg.exec_() == dlg.Accepted:
            method = dlg.get_selected_method()
            if method:
                self.on_payment_method_selected(method)
            else:
                QMessageBox.warning(self, "No Selection", "Please select a payment method.")

    def on_payment_method_selected(self, method):
        dlg = PaymentDetailsScreen(self.user, self.selected_package, method, self)
        if dlg.exec_() == dlg.Accepted:
            # Optionally handle post-payment logic here
            pass

    def on_payment_details_entered(self, details):
        if not self.validate_payment_details(details):
            self.show_invalid_payment_details()
            return
        if not self.user.has_sufficient_balance(details['amount']):
            self.show_inadequate_balance()
            return
        self.confirm_subscription()

    def confirm_subscription(self):
        # Ενημέρωση συνδρομής στη βάση και εμφάνιση ConfirmSubscriptionScreen
        pass

    def show_inadequate_balance(self):
        # Εμφάνιση οθόνης InadequateBalanceScreen
        pass

    def show_invalid_payment_details(self):
        # Εμφάνιση οθόνης InvalidPaymentDetailsScreen
        pass

    def show_my_subscriptions(self):
        # Εμφάνιση MySubscriptionsScreen με δυνατότητα ακύρωσης
        pass