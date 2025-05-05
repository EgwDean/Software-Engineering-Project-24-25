import services.Database as Database  # IMPORTANT, DO NOT OMIT
import entities.StandardUser as SU
import entities.Admin as AD
import sys
from PyQt5.QtWidgets import QApplication
from screens.LoginPage import LoginPage
from screens.HistoryPage import HistoryPage  # Import the new screen

def main():
    app = QApplication(sys.argv)

    login_page = LoginPage()
    login_page.show()

    def handle_login_success(user):
        login_page.close()
        if isinstance(user, SU.StandardUser):
            print(f"Welcome, {user.username}! You are logged in as a Standard User.")
            history = HistoryPage(user)
            history.show()
        elif isinstance(user, AD.Admin):
            print(f"Welcome, {user.username}! You are logged in as an Admin.")
            # You can open an Admin page here if needed

    login_page.login_successful.connect(handle_login_success)

    app.exec_()

if __name__ == "__main__":
    main()
