import services.Database as Database  # IMPORTANT, DO NOT OMIT
import entities.StandardUser as SU
import entities.Admin as AD
import sys
from PyQt5.QtWidgets import QApplication
from screens.LoginPage import LoginPage
<<<<<<< HEAD
from screens.HistoryPage import HistoryPage  # Import the new screen

=======
# Main function to start the application
>>>>>>> main
def main():
    app = QApplication(sys.argv)

    login_page = LoginPage()
    login_page.show()

    def handle_login_success(user):
    # Hide (don’t close) the login window so we can show it again later
        login_page.hide()

        if isinstance(user, SU.StandardUser):
            print(f"Welcome, {user.username}! You are logged in as a Standard User.")
            history = HistoryPage(user)

        # Connect the back_requested signal to close history & re-show login
            history.back_requested.connect(lambda: (
            history.close(),
            login_page.show()
                ))

            history.show()

        elif isinstance(user, AD.Admin):
            print(f"Welcome, {user.username}! You are logged in as an Admin.")

    login_page.login_successful.connect(handle_login_success)

    app.exec_()

if __name__ == "__main__":
    main()
