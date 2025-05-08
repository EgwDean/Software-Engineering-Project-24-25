import services.Database as Database
import entities.StandardUser as SU
import entities.Admin as AD
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from screens.LoginPage import LoginPage
from screens.HistoryPage import HistoryPage
from screens.BookPage import BookPage

def main():
    app = QApplication(sys.argv)

    login_page = LoginPage()
    login_page.show()

    def handle_login_success(user):
        login_page.hide()

        if isinstance(user, SU.StandardUser):
            print(f"Welcome, {user.username}! You are logged in as a Standard User.")

            # Connect to the database and fetch full listing by ID
            db = Database.Database()  # instantiate the class
            conn = db.connect()       # call the connect method on the instance
            if not conn:
                QMessageBox.critical(None, "Error", "Database connection failed.")
                return

            cur = conn.cursor(dictionary=True)
            try:
                listing_id = 1  # Replace this with dynamic logic if needed
                cur.execute("SELECT * FROM vehicle_listing WHERE id = %s", (listing_id,))
                listing = cur.fetchone()

                if not listing:
                    QMessageBox.critical(None, "Error", f"Listing with ID {listing_id} not found.")
                    return
            finally:
                cur.close()
                conn.close()

            # Show the booking page
            book_page = BookPage(user, listing)

            book_page.back_requested.connect(lambda: (
                book_page.close(),
                login_page.show()
            ))

            book_page.booking_confirmed.connect(lambda: (
                book_page.close(),
                login_page.show()  # or navigate elsewhere
            ))

            book_page.show()

        elif isinstance(user, AD.Admin):
            print(f"Welcome, {user.username}! You are logged in as an Admin.")
            # Admin flow (if needed)

    login_page.login_successful.connect(handle_login_success)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
