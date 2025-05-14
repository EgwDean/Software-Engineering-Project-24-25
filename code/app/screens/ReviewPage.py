from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
import services.Database as DB
from datetime import datetime

class ReviewPage(QDialog):
    def __init__(self, user, listing_id, parent=None):
        super().__init__(parent)
        self.user = user
        self.listing_id = listing_id
        self.rating = 0
        self.setWindowTitle("Submit Review")
        self.setFixedSize(400, 300)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Rating with clickable stars
        layout.addWidget(QLabel("Rating:"))
        stars_layout = QHBoxLayout()
        self.star_buttons = []
        for i in range(1, 6):
            btn = QPushButton('☆')
            btn.setFlat(True)
            btn.setStyleSheet(
                "QPushButton { font-size: 24px; color: #FFD700; border: none; }"
                "QPushButton:hover { color: #FFC107; }"
            )
            btn.setFixedSize(40, 40)
            btn.clicked.connect(lambda _, s=i: self._set_rating(s))
            self.star_buttons.append(btn)
            stars_layout.addWidget(btn)
        layout.addLayout(stars_layout)

        # Comment
        layout.addWidget(QLabel("Comment (max 250 chars):"))
        self.comment_edit = QTextEdit()
        self.comment_edit.setPlaceholderText("Write your review here...")
        self.comment_edit.setFixedHeight(100)
        layout.addWidget(self.comment_edit)

        # Submit
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_review)
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)

    def _set_rating(self, stars):
        self.rating = stars
        for idx, btn in enumerate(self.star_buttons, start=1):
            btn.setText('★' if idx <= stars else '☆')

    def submit_review(self):
        if self.rating == 0:
            QMessageBox.warning(self, "Error", "Please select a star rating.")
            return
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
                self.rating,
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