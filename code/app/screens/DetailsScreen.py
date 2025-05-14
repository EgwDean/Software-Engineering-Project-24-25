from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import services.Database as DB

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
        self.setMinimumSize(200, 100)

        layout = QVBoxLayout()
        label = QLabel(f"{brand} {model}")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(label)
        layout.addStretch()
        self.setLayout(layout)