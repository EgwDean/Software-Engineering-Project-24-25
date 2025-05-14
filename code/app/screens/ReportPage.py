
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
import services.Database as DB
from datetime import datetime

class ReportPage(QDialog):
    def __init__(self, user, listing_id, parent=None):
        super().__init__(parent)
        self.user = user
        self.listing_id = listing_id
        self.setWindowTitle("Submit Report")
        self.setFixedSize(500, 400)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Describe your report (max 1000 chars):"))
        self.report_edit = QTextEdit()
        self.report_edit.setPlaceholderText("Write your report here...")
        self.report_edit.setFixedHeight(250)
        layout.addWidget(self.report_edit)

        submit_btn = QPushButton("Submit Report")
        submit_btn.clicked.connect(self.submit_report)
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)

    def submit_report(self):
        report_text = self.report_edit.toPlainText().strip()
        if len(report_text) > 1000:
            QMessageBox.warning(self, "Error", "Report exceeds 1000 characters.")
            return

        db = DB.Database()
        conn = db.connect()
        if not conn:
            QMessageBox.critical(self, "Error", "Database connection failed.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reports (name_reporter, comment, date_of_report, id_list_report) "
                "VALUES (%s, %s, %s, %s)",
                (self.user.username,
                 report_text,
                 datetime.today().strftime('%Y-%m-%d'),
                 self.listing_id)
            )
            conn.commit()
            cursor.close()
            QMessageBox.information(self, "Success", "Report submitted successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to submit report: {e}")
        finally:
            conn.close()