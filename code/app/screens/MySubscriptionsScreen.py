from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QPushButton, QSizePolicy, QSpacerItem, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from services.ManageSubsClass import ManageSubsClass
from screens.CancelSubScreen import CancelSubScreen
from services.ManageCancelSubClass import ManageCancelSubClass

class MySubscriptionsScreen(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("My Subscription")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.showMaximized()

        # Outer layout to center the card
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(40, 40, 40, 40)
        outer_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(outer_layout)

        # Back button at the very top left
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        back_button = QPushButton("Back To Map")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #2a3f54;
                color: white;
                padding: 10px 0;
                border-radius: 6px;
                font-size: 15px;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #4682b4;
            }
        """)
        back_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        back_button.clicked.connect(self.goBackToMap)
        top_row.addWidget(back_button)
        top_row.addStretch()
        outer_layout.addLayout(top_row)

        # Fetch active subscription details using ManageSubsClass
        sub = ManageSubsClass.getActiveSubscriptionDetails(self.user.username)
        print("DEBUG: subscription details:", sub)

        if sub:
            card = QFrame()
            card.setMinimumWidth(400)
            card.setMaximumWidth(500)
            card.setMinimumHeight(320)
            card.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            card.setStyleSheet("""
                QFrame {
                    background: #f8fbff;
                    border-radius: 20px;
                    border: 2.5px solid #87ceeb;
                    padding: 32px;
                    margin: 10px;
                }
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(18)
            card_layout.setContentsMargins(16, 16, 16, 16)

            plan_label = QLabel(f"Subscription: {sub['plan']}")
            plan_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2a3f54;")
            plan_label.setAlignment(Qt.AlignCenter)

            price_label = QLabel(f"Price: €{sub['price']}")
            price_label.setStyleSheet("font-size: 22px; color: #28a745;")
            price_label.setAlignment(Qt.AlignCenter)

            commission_label = QLabel(f"Commission: {sub['commission']}%")
            commission_label.setStyleSheet("font-size: 18px; color: #555;")
            commission_label.setAlignment(Qt.AlignCenter)

            period_label = QLabel(f"Active: {sub['start_date']} to {sub['end_date']}")
            period_label.setStyleSheet("font-size: 18px; color: #555;")
            period_label.setAlignment(Qt.AlignCenter)

            cancel_btn = QPushButton("Cancel Subscription")
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #b22222;
                    color: white;
                    padding: 14px 0;
                    border-radius: 8px;
                    font-size: 18px;
                    margin-top: 16px;
                }
                QPushButton:hover {
                    background-color: #d9534f;
                }
            """)
            cancel_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            cancel_btn.clicked.connect(self.cancelSub)

            card_layout.addWidget(plan_label)
            card_layout.addWidget(price_label)
            card_layout.addWidget(commission_label)
            card_layout.addWidget(period_label)
            card_layout.addWidget(cancel_btn)

            # Add vertical spacers to center the card
            outer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
            outer_layout.addWidget(card, alignment=Qt.AlignCenter)
            outer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        else:
            no_sub_label = QLabel("No active subscription.")
            no_sub_label.setStyleSheet("font-size: 18px; color: #b00; font-weight: bold;")
            no_sub_label.setAlignment(Qt.AlignCenter)
            outer_layout.addWidget(no_sub_label)

    def goBackToMap(self):
        self.close()

    def cancelSub(self):
        # Show confirmation dialog
        self.cancel_dialog = CancelSubScreen(self)
        result = self.cancel_dialog.exec_()
        if result == QMessageBox.Yes:
            # User confirmed cancellation
            success = ManageCancelSubClass.cancelSub(self.user.username)
            if success:
                QMessageBox.information(self, "Canceled", "Your subscription has been canceled.")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Failed to cancel subscription. Please try again.")