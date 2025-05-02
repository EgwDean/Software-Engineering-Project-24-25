import services.Database as Database
import sys
from PyQt5.QtWidgets import QApplication
from screens.LoginPage import LoginPage

# Run the app
if __name__ == "__main__":

    # Connect to the database
    db = Database.Database()
    db.connect()

    # Show the login page
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())