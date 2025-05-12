from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class ListEditingScreen(QWidget):
    def __init__(self, user, listing_data):
        super().__init__()
        self.user = user
        self.listing_data = listing_data  # Αποθήκευση των δεδομένων της αγγελίας
        self.setWindowTitle("Edit Listing")
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout()

        # Εμφάνιση του τίτλου της αγγελίας (brand, model, year)
        title_label = QLabel(f"{self.listing_data['brand']} {self.listing_data['model']} ({self.listing_data['year']})")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)

        # Εμφάνιση της περιγραφής της αγγελίας
        description_label = QLabel(f"Description: {self.listing_data['description']}")
        description_label.setStyleSheet("font-size: 18px; color: #666;")
        layout.addWidget(description_label)

        # Δημιουργία πεδίων για επεξεργασία
        self.description_input = QLineEdit(self)
        self.description_input.setText(self.listing_data['description'])  # Προεπιλεγμένο κείμενο από την αγγελία
        self.description_input.setPlaceholderText("Edit description")
        layout.addWidget(self.description_input)

        # Προσθήκη κουμπιού για αποθήκευση αλλαγών
        save_button = QPushButton("Save Changes")
        save_button.setStyleSheet("""
            padding: 12px 20px;
            background-color: #28a745;
            color: white;
            border-radius: 5px;
            font-size: 14px;
        """)
        layout.addWidget(save_button)

        self.setLayout(layout)
