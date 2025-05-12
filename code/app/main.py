import services.Database as Database  # IMPORTANT, DO NOT OMIT
import entities.StandardUser as SU
import entities.Admin as AD
import sys
from PyQt5.QtWidgets import QApplication
from screens.LoginPage import LoginPage
# Main function to start the application
def main():
    app = QApplication(sys.argv)

    # Start with the LoginPage
    login_page = LoginPage()
    login_page.show()

    # Wait for the login process to complete
    app.exec_()

    # Handle the returned object from the login process
    user = login_page.login()
    if isinstance(user, SU.StandardUser):
        print(f"Welcome, {user.username}! You are logged in as a Standard User.")
    elif isinstance(user, AD.Admin):
        print(f"Welcome, {user.username}! You are logged in as an Admin.")
    else:
        print("Login failed or canceled.")

if __name__ == "__main__":
    main()