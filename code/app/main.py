import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
import services.Database as Database
import entities.StandardUser as SU
import entities.Admin as AD
from screens.LoginPage import LoginPage
from screens.MapScreen import MapScreen

# Keep windows alive
_open_windows = {}

def main():
    app = QApplication(sys.argv)

    login_page = LoginPage()
    print("Showing login page")
    login_page.show()

    def handle_login_success(user):
        print("handle_login_success called with:", user)
        login_page.hide()

        if isinstance(user, SU.StandardUser):
            print(f"Welcome, {user.username}! Launching MapScreen.")
            # Store it so Python doesn't garbage‐collect
            _open_windows['map'] = MapScreen(user)
            _open_windows['map'].show()

        elif isinstance(user, AD.Admin):
            print(f"Welcome, {user.username}! Admin flow placeholder.")
            QMessageBox.information(None, "Admin", "Admin dashboard not implemented.")

    # Connect signal **before** you ever call show()
    login_page.login_successful.connect(handle_login_success)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
