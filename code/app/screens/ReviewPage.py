from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt
import services.Database as DB
from datetime import datetime

class ReviewPage(QDialog):
    def __init__(self, user, listing_id, parent=None):
        super().__init__(parent)
        self.user = user
        self.listing_id = listing_id
        self.setWindowTitle("Submit Review")
        self.setFixedSize(400, 300)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Rating (1 to 5):"))
        self.stars_combo = QComboBox()
        self.stars_combo.addItems([str(i) for i in range(1, 6)])
        layout.addWidget(self.stars_combo)

        layout.addWidget(QLabel("Comment (max 250 chars):"))
        self.comment_edit = QTextEdit()
        self.comment_edit.setPlaceholderText("Write your review here...")
        self.comment_edit.setFixedHeight(100)
        layout.addWidget(self.comment_edit)

        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_review)
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)

    def submit_review(self):
        comment = self.comment_edit.toPlainText().strip()
        if len(comment) > 250:
            QMessageBox.warning(self, "Error", "Comment exceeds 250 characters.")
            return

        db = DB.Database()
        conn = db.connect()
        if not conn:
            QMessageBox.critical(self, "Error", "Database connection failed.")
            return

        try:
            cursor = conn.cursor()
            insert = (
                "INSERT INTO reviews "
                "(name_reviewer, id_list_review, stars, comment, date_of_review) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            cursor.execute(insert, (
                self.user.username,
                self.listing_id,
                int(self.stars_combo.currentText()),
                comment,
                datetime.today().strftime('%Y-%m-%d')
            ))
            conn.commit()
            cursor.close()
            QMessageBox.information(self, "Success", "Review submitted successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to submit review: {e}")
        finally:
            conn.close()
