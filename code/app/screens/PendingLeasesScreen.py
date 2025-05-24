from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QScrollArea
from PyQt5.QtCore import Qt
import services.Database as DB
from screens.AcceptDeclineMenu import AcceptDeclineMenu
import functools

class PendingLeasesScreen(QWidget):
    def __init__(self, owner_user, parent=None):
        super().__init__(parent)
        self.owner_user = owner_user
        self.setWindowTitle("Pending Leases")
        self.setStyleSheet("background-color: #f5f5f5;")
        self._init_ui()
        self.showMaximized()  # Add this line to maximize the window

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        title = QLabel("Pending Lease Requests")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #007BFF; margin: 20px;")
        main_layout.addWidget(title, alignment=Qt.AlignCenter)

        # Scroll area for leases
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        self.leases_layout = QVBoxLayout(content)
        self.refreshLeases()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def refreshLeases(self):
        # Clear previous
        while self.leases_layout.count():
            item = self.leases_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        leases = self.fetchPendingLeases()
        if not leases:
            lbl = QLabel("No pending leases.")
            lbl.setStyleSheet("font-size: 18px; color: #999; margin: 40px;")
            lbl.setAlignment(Qt.AlignCenter)  # Center the label horizontally
            self.leases_layout.addStretch()
            self.leases_layout.addWidget(lbl, alignment=Qt.AlignCenter)
            self.leases_layout.addStretch()
            return

        for lease in leases:
            box = QFrame()
            box.setStyleSheet("background: white; border: 1px solid #ddd; border-radius: 8px; margin: 10px; padding: 15px;")
            layout = QHBoxLayout(box)

            info = QVBoxLayout()
            info.addWidget(QLabel(f"<b>User:</b> {lease['user_who_rents']}"))
            info.addWidget(QLabel(f"<b>Car:</b> {lease['brand']} {lease['model']} ({lease['year']})"))
            info.addWidget(QLabel(f"<b>From:</b> {lease['from_date']}"))
            info.addWidget(QLabel(f"<b>Days:</b> {lease['number_of_days']}"))
            layout.addLayout(info)

            btn = QPushButton("View Lease")
            btn.setStyleSheet("padding: 10px 20px; background: #007BFF; color: white; border-radius: 5px; font-size: 14px;")
            btn.clicked.connect(functools.partial(self.chooseLease, lease))
            layout.addWidget(btn)

            self.leases_layout.addWidget(box)
        self.leases_layout.addStretch()

    def fetchPendingLeases(self):
        # Fetch all pending leases for listings owned by this user
        db = DB.Database()
        conn = db.connect()
        if not conn:
            return []
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT r.*, v.brand, v.model, v.year, v.name_of_user, v.price_per_day
                FROM rents r
                JOIN vehicle_listing v ON r.id_of_listing = v.id
                WHERE v.name_of_user = %s AND r.status = 'pending'
                ORDER BY r.from_date DESC
            """, (self.owner_user.username,))
            leases = cur.fetchall()
            cur.close()
            return leases
        finally:
            conn.close()

    def chooseLease(self, lease):
        print("Button pressed! Lease:", lease)
        self.accept_decline_menu = AcceptDeclineMenu(lease, parent=self)
        self.accept_decline_menu.exec_()
        self.refreshLeases()  # Refresh the list after dialog closes