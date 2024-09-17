from PyQt6.QtWidgets import QMainWindow
from screens.DetailsScreen import DetailsScreen

class HomeScreen(QMainWindow):
    def __init__(self, appState, parent=None):
        super(HomeScreen, self).__init__()

        self.app_state = appState
        self.ui = "ui/home.ui"
        self.father = parent

        self.app_state.loadUI(self.ui, self)
        self.setObjectName("HomeScreen")

        self.btnWyjazdy.clicked.connect(lambda: self.app_state.WyjazdyScreen.print_records())
        self.btnCzlonkowie.activated.connect(self.fun)

    def fun(self):
        x = DetailsScreen(self.app_state, empty=True)
        x.show()