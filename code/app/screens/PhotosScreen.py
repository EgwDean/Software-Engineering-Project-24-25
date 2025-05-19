from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
import services.Database as DB

class PhotosScreen(QWidget):
    def __init__(self, user, data, parent=None):
        super().__init__(parent)
        self.user = user
        self.data = data  # Dictionary with the form fields

        self.setWindowTitle("Upload Photos")
        self.setMinimumSize(400, 300)

        # Fetch the next listing id
        self.next_listing_id = self.get_next_listing_id()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Center frame
        frame = QFrame()
        frame.setStyleSheet("background: white; border-radius: 10px;")
        frame.setFixedWidth(400)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel("Enter Photos")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        frame_layout.addWidget(title)

        # Photos button
        photos_btn = QPushButton("Photos")
        photos_btn.setStyleSheet(
            "background-color: skyblue; color: white; font-weight: bold; padding: 10px 24px; margin: 20px 0;"
        )
        frame_layout.addWidget(photos_btn, alignment=Qt.AlignCenter)

        # Buttons (Cancel and Next)
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(
            "background-color: skyblue; color: white; font-weight: bold; padding: 8px 24px;"
        )
        cancel_btn.clicked.connect(self.cancel)

        next_btn = QPushButton("Next")
        next_btn.setStyleSheet(
            "background-color: skyblue; color: white; font-weight: bold; padding: 8px 24px;"
        )
        # next_btn.clicked.connect(self.next_step)  # To be implemented

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(next_btn)
        frame_layout.addLayout(button_layout)

        main_layout.addWidget(frame, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)
        self.showMaximized()

    def get_next_listing_id(self):
        try:
            db = DB.Database()
            connection = db.connect()
            if connection is None:
                return 1
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(id) FROM vehicle_listing")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            if result and result[0] is not None:
                return result[0] + 1
            else:
                return 1
        except Exception as e:
            print(f"Error fetching next listing id: {e}")
            return 1

    def cancel(self):
        self.close()