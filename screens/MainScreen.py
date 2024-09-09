from PyQt6 import QtWidgets as qtw 
from PyQt6.QtCore import QSize
from colorama import Fore

class MainScreen(qtw.QMainWindow):
    def __init__(self, appState):
        super(MainScreen, self).__init__()
        self.setWindowTitle("OSP PANEL")
        self.app_state = appState        # Connecting AppState class to a window
        self.dataObject = self.app_state.dataObject
        self.ui = "ui/login.ui"
        self.app_state.loadUI(self.ui, self, QSize(870, 543))
        self.submit.clicked.connect(self.logIN)

    def logIN(self) -> None:
        login = self.loginField.text()
        password = self.passField.text()

        login_OK = self.dataObject.verify_user(login, password)

        if login_OK or login == '':
            self.app_state.loadWidget(self.app_state.HomeScreen)
        else:
            self.create_messageBox()

    def create_messageBox(self) -> None:
        print(f"{Fore.RED}Login failed. Incorret email or password{Fore.RESET}")
        # Creating a message box if login failed
        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText('Login failed')
        msg.setInformativeText("Incorrect login or passowrd")
        msg.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
        msg.exec()
        self.loginField.setText("")
        self.passField.setText("")