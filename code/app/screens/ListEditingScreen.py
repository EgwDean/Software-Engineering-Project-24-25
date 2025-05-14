from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QMessageBox
from PyQt5.QtCore import QDate
import services.Database as DB

class ListEditingScreen(QWidget):
    def __init__(self, user, listing_data, parent=None):
        super().__init__(parent)
        self.user = user
        self.listing_data = listing_data
        self.setWindowTitle("Edit Listing")
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout()

        # --- Brand, Model, Year Title
        title_label = QLabel(f"{self.listing_data['brand']} {self.listing_data['model']} ({self.listing_data['year']})")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)

        # --- Input fields for editable data
        self.price_input = QLineEdit(str(self.listing_data["price_per_day"]))
        self.price_input.setPlaceholderText("Price per day")
        layout.addWidget(QLabel("Price per Day:"))
        layout.addWidget(self.price_input)

        self.vehicle_type_input = QLineEdit(self.listing_data["vehicle_type"])
        layout.addWidget(QLabel("Vehicle Type:"))
        layout.addWidget(self.vehicle_type_input)

        self.brand_input = QLineEdit(self.listing_data["brand"])
        layout.addWidget(QLabel("Brand:"))
        layout.addWidget(self.brand_input)

        self.model_input = QLineEdit(self.listing_data["model"])
        layout.addWidget(QLabel("Model:"))
        layout.addWidget(self.model_input)

        self.year_input = QLineEdit(str(self.listing_data["year"]))
        layout.addWidget(QLabel("Year:"))
        layout.addWidget(self.year_input)

        self.km_input = QLineEdit(str(self.listing_data["total_km"]))
        layout.addWidget(QLabel("Total Kilometers:"))
        layout.addWidget(self.km_input)

        self.fuel_input = QLineEdit(self.listing_data["fuel_type"])
        layout.addWidget(QLabel("Fuel Type:"))
        layout.addWidget(self.fuel_input)

        self.description_input = QLineEdit(self.listing_data["description"])
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)

        self.from_date_input = QDateEdit()
        self.from_date_input.setDate(QDate.fromString(str(self.listing_data["from_date"]), "yyyy-MM-dd"))
        layout.addWidget(QLabel("From Date:"))
        layout.addWidget(self.from_date_input)

        self.to_date_input = QDateEdit()
        self.to_date_input.setDate(QDate.fromString(str(self.listing_data["to_date"]), "yyyy-MM-dd"))
        layout.addWidget(QLabel("To Date:"))
        layout.addWidget(self.to_date_input)

        self.status_input = QLineEdit(self.listing_data["status"])
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.status_input)

        # --- Save Button
        save_button = QPushButton("Save Changes")
        save_button.setStyleSheet("""
            padding: 12px 20px;
            background-color: #28a745;
            color: white;
            border-radius: 5px;
            font-size: 14px;
        """)
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        # --- Delete Button
        delete_button = QPushButton("Delete Listing")
        delete_button.setStyleSheet("""
            padding: 12px 20px;
            background-color: #dc3545;
            color: white;
            border-radius: 5px;
            font-size: 14px;
        """)
        delete_button.clicked.connect(self.delete_listing)
        layout.addWidget(delete_button)

        self.setLayout(layout)

    def validate_listing(self):
        fields = [
            self.price_input.text(),
            self.vehicle_type_input.text(),
            self.brand_input.text(),
            self.model_input.text(),
            self.year_input.text(),
            self.km_input.text(),
            self.fuel_input.text(),
            self.description_input.text(),
            self.from_date_input.date().toString("yyyy-MM-dd"),
            self.to_date_input.date().toString("yyyy-MM-dd"),
            self.status_input.text()
        ]
        
        for field in fields:
            if not field.strip():
                return False
        return True

    def save_changes(self):
        if not self.validate_listing():
            print("Please fill in all fields.")
            return

        try:
            db = DB.Database()
            conn = db.connect()

            if conn is None:
                print("Database connection failed.")
                return

            cursor = conn.cursor()

            query = """
                UPDATE vehicle_listing
                SET price_per_day = %s,
                    vehicle_type = %s,
                    brand = %s,
                    model = %s,
                    year = %s,
                    total_km = %s,
                    fuel_type = %s,
                    description = %s,
                    from_date = %s,
                    to_date = %s,
                    status = %s
                WHERE id = %s AND name_of_user = %s
            """

            values = (
                float(self.price_input.text()),
                self.vehicle_type_input.text(),
                self.brand_input.text(),
                self.model_input.text(),
                int(self.year_input.text()),
                int(self.km_input.text()),
                self.fuel_input.text(),
                self.description_input.text(),
                self.from_date_input.date().toString("yyyy-MM-dd"),
                self.to_date_input.date().toString("yyyy-MM-dd"),
                self.status_input.text(),
                self.listing_data["id"],
                self.user.username
            )

            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            print("Changes saved successfully.")

            # Εμφάνιση του Popup
            self.show_popup()

        except Exception as e:
            print(f"Error saving changes: {e}")

    def show_popup(self):
        # Δημιουργία του Popup για την επιβεβαίωση
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("UpdateScreen")
        msg.setText("Your listing has been updated successfully!")
        msg.setStandardButtons(QMessageBox.Ok)  # Προσθήκη κουμπιού OK
        msg.buttonClicked.connect(self.close_and_return)  # Σύνδεση κουμπιού με την ενέργεια
        msg.exec_()

    def close_and_return(self, button):
        self.close()  # Κλείσιμο της τρέχουσας οθόνης
        if self.parent():  # Ελέγχουμε αν υπάρχει γονέας
            self.parent().show()  # Επιστροφή στην προηγούμενη οθόνη

    def delete_listing(self):
        # Δημιουργία του Popup για επιβεβαίωση διαγραφής
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("AttentionScreen")
        msg.setText(f"Are you sure you want to delete the listing: {self.listing_data['brand']} {self.listing_data['model']} ({self.listing_data['year']})?")
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        msg.buttonClicked.connect(self.confirm_delete)
        msg.exec_()

    def confirm_delete(self, button):
        if button.text() == "OK":
            try:
                db = DB.Database()
                conn = db.connect()
                if conn is None:
                    print("Database connection failed.")
                    return

                cursor = conn.cursor()
                query = "UPDATE vehicle_listing SET status = 'deleted' WHERE id = %s AND name_of_user = %s;"
                cursor.execute(query, (self.listing_data["id"], self.user.username))
                conn.commit()
                cursor.close()
                conn.close()
                print("Listing deleted successfully.")

                # Κλείσιμο της οθόνης και επιστροφή στην προηγούμενη οθόνη
                self.close()
                if self.parent():
                    self.parent().show()

            except Exception as e:
                print(f"Error deleting listing: {e}")