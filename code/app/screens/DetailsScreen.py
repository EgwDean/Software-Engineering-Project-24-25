from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import services.Database as DB
import os

class DetailsScreen(QWidget):
    def __init__(self, listing_id, parent=None):
        super().__init__(parent)
        brand = "Unknown"
        model = "Unknown"

        try:
            db = DB.Database()
            connection = db.connect()
            if connection:
                cursor = connection.cursor()
                query = "SELECT brand, model FROM vehicle_listing WHERE id = %s"
                cursor.execute(query, (listing_id,))
                result = cursor.fetchone()
                if result:
                    brand, model = result
                cursor.close()
                connection.close()
        except Exception as e:
            print(f"Error fetching listing details: {e}")

        self.setWindowTitle("Vehicle Details")
        self.setMinimumSize(300, 300)

        layout = QVBoxLayout()

        # Brand and model label
        label = QLabel(f"{brand} {model}")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(label)

        # Image loading
        image_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "assets", "images", f"img_{listing_id}_1.jpg"
        )
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            image_label.setAlignment(Qt.AlignHCenter)
            layout.addWidget(image_label)
        else:
            image_label = QLabel("No image available")
            image_label.setAlignment(Qt.AlignHCenter)
            layout.addWidget(image_label)

        # Show More button
        show_more_btn = QPushButton("Show More")
        show_more_btn.setStyleSheet(
            """
            QPushButton {
                background-color: skyblue;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 8px 0;
                outline: none;
            }
            QPushButton:focus {
                outline: none;
            }
            """
        )
        show_more_btn.clicked.connect(self.showMore)
        layout.addWidget(show_more_btn, alignment=Qt.AlignHCenter)

        layout.addStretch()
        self.setLayout(layout)

    def showMore(self):
        pass