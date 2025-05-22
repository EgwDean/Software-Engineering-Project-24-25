from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
import services.Database as DB
import os
import shutil
from screens.CompletionScreen import CompletionScreen  # Add this import at the top if CompletionScreen exists

class PhotosScreen(QWidget):
    def __init__(self, user, data, parent=None):
        super().__init__(parent)
        self.user = user
        self.data = data  # Dictionary with the form fields
        self.selected_photos = []

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

        # Notification label (hidden by default)
        self.notify_label = QLabel("please select at least one photo")
        self.notify_label.setStyleSheet("color: red; font-weight: bold;")
        self.notify_label.setAlignment(Qt.AlignCenter)
        self.notify_label.hide()
        frame_layout.insertWidget(1, self.notify_label)  # Show below the title

        # Photos button
        photos_btn = QPushButton("Photos")
        photos_btn.setStyleSheet(
            "background-color: skyblue; color: white; font-weight: bold; padding: 10px 24px; margin: 20px 0;"
        )
        photos_btn.clicked.connect(self.enterPhotos)
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
        next_btn.clicked.connect(self.checkPhotos)

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

    def enterPhotos(self):
        # Open file dialog for jpg files only
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select JPG Photos",
            "",
            "JPEG Images (*.jpg *.jpeg)"
        )
        if files:
            listing_id = self.get_next_listing_id()
            saved_photos = []
            # Create the temp directory inside code/assets
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # .../code
            photos_dir = os.path.join(base_dir, "assets", "temp")
            if not os.path.exists(photos_dir):
                os.makedirs(photos_dir)
            for idx, file_path in enumerate(files, start=1):
                ext = os.path.splitext(file_path)[1].lower()
                if ext in [".jpg", ".jpeg"]:
                    new_filename = f"img_{listing_id}_{idx}.jpg"
                    dest_path = os.path.join(photos_dir, new_filename)
                    shutil.copy(file_path, dest_path)
                    saved_photos.append(dest_path)
            self.selected_photos = saved_photos
            print("Saved photos:", self.selected_photos)
            print("Listing id:", listing_id)
            # Pass self.selected_photos, self.user, self.data to the next class when needed

    def photosNotify(self):
        self.notify_label.show()

    def checkPhotos(self):
        if not self.selected_photos:
            self.photosNotify()
        else:
            self.notify_label.hide()
            self.completion_screen = CompletionScreen(self.user, self.data, self.selected_photos)
            self.completion_screen.show()
            self.close()

    def cancel(self):
        self._should_empty_temp = True
        self.close()

    def closeEvent(self, event):
        # Only empty temp if self._should_empty_temp is True (set by cancel or X)
        if getattr(self, "_should_empty_temp", False):
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            temp_dir = os.path.join(base_dir, "assets", "temp")
            if os.path.exists(temp_dir):
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")
        super().closeEvent(event)