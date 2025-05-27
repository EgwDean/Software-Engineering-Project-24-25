from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QPushButton, QMessageBox, QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt
import services.Database as DB
from services.ManageSubsClass import ManageSubsClass
from screens.SelectPaymentMethodScreen import SelectPaymentMethodScreen
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
        back_button.clicked.connect(self.goBackToMap)
        self.main_layout.addWidget(back_button)

        # Use ManageSubsClass for subscription check
        if ManageSubsClass.checkSub(self.user.username):
            self.show_my_subscriptions()
        else:
            self.displayPackages()

    def goBackToMap(self):
        self.close()

    def displayPackages(self):
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
            select_btn.clicked.connect(lambda _, p=plan: self.chooseSub(p))

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

    def chooseSub(self, package):
        self.selected_package = package
        dlg = SelectPaymentMethodScreen(self)
        if dlg.exec_() == dlg.Accepted:
            method = dlg.chooseMethod()
            if method:
                payment_dlg = PaymentDetailsScreen(self.user, self.selected_package, method, self)
                if payment_dlg.exec_() == payment_dlg.Accepted:
                    pass  # Optionally handle post-payment logic here
            else:
                QMessageBox.warning(self, "No Selection", "Please select a payment method.")
