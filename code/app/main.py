import sys
from PyQt5.QtWidgets import QApplication
from screens.LoginPage import LoginPage

# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    app.exec_()