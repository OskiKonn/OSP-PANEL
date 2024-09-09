from PyQt6.QtWidgets import QMainWindow
from colorama import Fore
from data_model import TableModel
from DetailsScreen import DetailsScreen

class WyjazdyScreen(QMainWindow):
    def __init__(self, appState, parent=None):
        super(WyjazdyScreen, self).__init__()
            
        self.app_state = appState
        self.dataObject = self.app_state.dataObject
        self.father = parent
        self.ui = "ui/wyjazdy.ui"
        self.detail_windows: list = []
        self.app_state.loadUI(self.ui, self)
        self.initialized: bool = False

    def print_wyjazdy(self) -> None:

        print(f"{Fore.YELLOW}Fetching...{Fore.RESET}")
        data_fetch_OK, data = self.dataObject.fetch_table_data("wyjazdy")

        if not data_fetch_OK:
            print(data)         # Prints error message (in that case data is a hardcoded string)
        else:
            list_data = data
            self.model = TableModel(list_data, True)
            self.list.setModel(self.model)                   # Setting data model to a list of wyjazdy
            self.list.resizeColumnsToContents()
            if not self.initialized:
                self.list.doubleClicked.connect(self.showDetails)
                self.initialized = True
            self.app_state.loadWidget(self.app_state.WyjazdyScreen)

    def showDetails(self, index) -> None:
        id = self.model.returnId(index.row())
        wyjazd_details = DetailsScreen(self.app_state, id)
        self.detail_windows.append(wyjazd_details)      # Pushes widget to a list of active widgets
        wyjazd_details.show()                           # makes it possible to have more than one opened