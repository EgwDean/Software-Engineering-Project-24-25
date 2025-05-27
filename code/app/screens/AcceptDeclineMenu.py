from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import services.Database as DB
from screens.LeaseConfirmScreen import LeaseConfirmScreen
from services.ManageAcceptClass import ManageAcceptClass
from services.ManageDeclineClass import ManageDeclineClass

class AcceptDeclineMenu(QDialog): 
    def __init__(self, lease, parent=None):
        super().__init__(parent)
        self.lease = lease
        self.setWindowTitle("Lease Request Details")
        self.setStyleSheet("background-color: #f5f5f5;")
        self._init_ui()
        self.resize(700, 500)  # Set the dialog to a larger, but not full, size

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Lease info
        layout.addWidget(QLabel(f"<b>User:</b> {self.lease['user_who_rents']}"))
        layout.addWidget(QLabel(f"<b>Car:</b> {self.lease['brand']} {self.lease['model']} ({self.lease['year']})"))
        layout.addWidget(QLabel(f"<b>From:</b> {self.lease['from_date']}"))
        layout.addWidget(QLabel(f"<b>Days:</b> {self.lease['number_of_days']}"))

        # Accept and Decline buttons
        btn_accept = QPushButton("Accept")
        btn_accept.setStyleSheet("background: #28a745; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        btn_accept.clicked.connect(self.acceptLease)
        layout.addWidget(btn_accept)

        btn_decline = QPushButton("Decline")
        btn_decline.setStyleSheet("background: #dc3545; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        btn_decline.clicked.connect(self.declineLease)
        layout.addWidget(btn_decline)

    def acceptLease(self):
        # Inline updateLeaseStatus logic
        db = DB.Database()
        conn = db.connect()
        if not conn:
            QMessageBox.critical(self, "Database Error", "Could not connect to the database.")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE rents SET status = %s WHERE id_of_listing = %s AND user_who_rents = %s",
                ('accepted', self.lease['id_of_listing'], self.lease['user_who_rents'])
            )
            conn.commit()
            cur.close()
        finally:
            conn.close()

        ok, msg = ManageAcceptClass.checkSub(self.lease)
        if ok:
            confirm_screen = LeaseConfirmScreen(self)
            confirm_screen.exec_()
        else:
            QMessageBox.critical(self, "Error", msg or "Failed to process acceptance.")
        self.close()

    def declineLease(self):
        # Inline updateLeaseStatus logic
        db = DB.Database()
        conn = db.connect()
        if not conn:
            QMessageBox.critical(self, "Database Error", "Could not connect to the database.")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE rents SET status = %s WHERE id_of_listing = %s AND user_who_rents = %s",
                ('declined', self.lease['id_of_listing'], self.lease['user_who_rents'])
            )
            conn.commit()
            cur.close()
        finally:
            conn.close()

        ok, msg = ManageDeclineClass.returnLeseeAmount(self.lease)
        if ok:
            QMessageBox.information(self, "Lease Declined", "You have declined the lease request and refunded the user.")
        else:
            QMessageBox.critical(self, "Error", msg or "Failed to process decline/refund.")
        self.close()