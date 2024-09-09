from PyQt6.QtWidgets import QMainWindow

class HomeScreen(QMainWindow):
    def __init__(self, appState, parent=None):
        super(HomeScreen, self).__init__()

        self.app_state = appState
        self.ui = "ui/home.ui"
        self.father = parent

        self.app_state.loadUI(self.ui, self)
        self.setObjectName("HomeScreen")

        self.btnWyjazdy.clicked.connect(lambda: self.app_state.WyjazdyScreen.print_wyjazdy())
        self.btnCzlonkowie.activated.connect(self.fun)

    def fun(self):
        print("Dziala")