from PyQt6.QtWidgets import QMainWindow

class HomeScreen(QMainWindow):
    def __init__(self, app, parent=None):
        super(HomeScreen, self).__init__()

        self.app = app
        self.ui = "ui/home.ui"
        self.father = parent

        self.app.loadUI(self.ui, self)
        self.setObjectName("HomeScreen")

        self.btnWyjazdy.clicked.connect(lambda: self.app.RecordsScreen.print_records())