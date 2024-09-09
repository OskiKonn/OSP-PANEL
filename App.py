import sys
import requests
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QStackedWidget, QMainWindow, QWidget, QLineEdit, QComboBox
from PyQt6.QtCore import QSize
from colorama import Fore, init # color prints module
from typing import Literal
# Import data_model classes
from data_model import FetchData, TableModel, ValueInjector
# Importing Screens modules
from screens.MainScreen import MainScreen
from screens.HomeScreen import HomeScreen
from screens.WyjazdyScreen import WyjazdyScreen


class AppState(QMainWindow):
    def __init__(self):
        super(AppState, self).__init__()
        print(f"{Fore.GREEN}AppState loaded{Fore.RESET}")

        # Creating data-fetching object
        self.dataObject = FetchData("http://localhost")

        # Initializing Widgets
        self.MainScreen = MainScreen(self)
        self.HomeScreen = HomeScreen(self)
        self.WyjazdyScreen = WyjazdyScreen(self, self.HomeScreen)

        # Adding widgets to stack
        self.screens = QStackedWidget()
        self.screens.addWidget(self.MainScreen)
        self.screens.addWidget(self.HomeScreen)
        self.screens.addWidget(self.WyjazdyScreen)
        print(f"{Fore.YELLOW}Stack loaded succesfully{Fore.RESET}")
        self.loadWidget(self.MainScreen)


    # loading GUI page
    def loadUI(self, file: str, window: QWidget | QMainWindow, size: QSize | None = None) -> None:

        if size == None:
            size = window.size()

        try:
            uic.loadUi(file, window)
            window.resize(size)

            if hasattr(window, "father") and window.father is not None:             # Checks if class has a parent attribute
                window.go_back.clicked.connect(lambda: self.goBack(window.father))  # if there's not parent then nowhere to go
            else:
                pass

            print(f"{Fore.GREEN}UI loaded succesfully - ({file}){Fore.RESET}")

        except Exception as e:
            print(f"{Fore.RED}loading UI Failed - ({file})\nError: {e}{Fore.RESET}")


    # loading widget
    def loadWidget(self, widget: QWidget | QMainWindow) -> None:

        self.screens.setCurrentWidget(widget)

        try:
            self.setCentralWidget(self.screens)        # Setting view to the currently active widget in stack
            print(f"{Fore.GREEN}Succesfully loaded widget - ({widget.objectName()}){Fore.RESET}")

        except Exception as e:
            print(f"{Fore.RED}Failed loading widget - ({widget})\nWith Error: {e}{Fore.RESET}")



    def goBack(self, parent: QWidget | QMainWindow):
        self.loadWidget(parent)

def main () -> None:
    init(True)
    app = QApplication(sys.argv)
    main_window = AppState()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()