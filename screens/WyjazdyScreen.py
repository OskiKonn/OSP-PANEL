from PyQt6.QtWidgets import QMainWindow
from colorama import Fore
from data_model import TableModel
from screens.DetailsScreen import DetailsWyjazdy

class WyjazdyScreen(QMainWindow):
    def __init__(self, appState, parent=None):
        super(WyjazdyScreen, self).__init__()
            
        self.app_state = appState
        self.dataObject = self.app_state.dataObject
        self.father = parent
        self.ui = "ui/wyjazdy.ui"
        self.app_state.loadUI(self.ui, self)
        self.initialized: bool = False
        self.add.clicked.connect(self.add_record)

    def print_records(self) -> None:

        print(f"{Fore.YELLOW}Fetching...{Fore.RESET}")
        data_fetch_OK, data = self.dataObject.fetch_table_data("wyjazdy")

        if not data_fetch_OK:
            print(data)         # Prints error message (in that case data is a hardcoded string)
        else:
            self.model = TableModel(data, True)
            self.list.setModel(self.model)                   # Setting data model to a list of wyjazdy
            self.list.resizeColumnsToContents()

            if not self.initialized:
                self.list.doubleClicked.connect(self.showDetails)
                self.initialized = True

            self.app_state.loadWidget(self.app_state.WyjazdyScreen)

    def showDetails(self, index) -> None:
        id = self.model.returnId(index.row())
        details = DetailsWyjazdy(self.app_state, id)
        details.show()                           # makes it possible to have more than one opened

    def add_record(self) -> None:
        def update_data() -> None:
            _, new_data = self.dataObject.fetch_table_data("wyjazdy")
            self.model.refresh(new_data)
            
        new_record = DetailsWyjazdy(self.app_state, empty=True)
        new_record.record_added.connect(update_data)
        new_record.show()
