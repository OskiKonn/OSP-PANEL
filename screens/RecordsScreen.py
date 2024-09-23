from PyQt6.QtWidgets import QMainWindow
from colorama import Fore
from data_model import TableModel
from screens.DetailsScreen import DetailsWyjazdy, DetailsScreen
from typing import Literal

class RecordsScreen(QMainWindow):

    details_map : dict = {
        "wyjazdy" : DetailsWyjazdy,
        "czlonkowie" : DetailsWyjazdy
    }

    def __init__(self, appState, section: Literal["wyjazdy", "czlonkowie", "wyposazenie", "dokumenty"], parent=None):
        super(RecordsScreen, self).__init__()        
        self.app_state = appState
        self.section = section
        if parent is not None:
            self.father = parent

        self.dataObject = self.app_state.dataObject
        self.app_state.loadUI("ui/records.ui", self)
        self.initialized: bool = False
        self.title.setText(self.section.upper())
        self.add.clicked.connect(self.add_record)


    def print_records(self) -> None:

        print(f"{Fore.YELLOW}Fetching...{Fore.RESET}")
        data_fetch_OK, data = self.dataObject.fetch_table_data(self.section)

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
        screen : QMainWindow = self.get_details_screen
        details = screen(self.app_state, self, id)
        details.show()

    def add_record(self) -> None:
        screen: QMainWindow = self.get_details_screen
        new_record = screen(self.app_state, self, empty=True)
        new_record.show()
    
    @property
    def get_details_screen(self) -> QMainWindow:
        screen : QMainWindow = RecordsScreen.details_map.get(self.section)

        if screen is None:
            raise ValueError(f"{Fore.RED}Nie ma takiej sekcji{Fore.RESET}")
        
        return screen

