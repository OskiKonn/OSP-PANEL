from data_model import ValueInjector
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QSize

class DetailsScreen(QWidget):
    def __init__(self, appState, record_id: int):
        super(DetailsScreen, self).__init__()
        self.app_state = appState
        self.dataObject = self.app_state.dataObject
        self.id = record_id
        self.ui = "ui/wyjazd_details.ui"
        self.app_state.loadUI(self.ui, self, QSize(800, 700))
        self.setWindowTitle(f"Wyjazd nr: {self.id}")
        self.closeBtn.clicked.connect(lambda: self.close())
        self.injector_initialized: bool = False
        self.combos = (self.commander, self.driver, self.ratownik1, self.ratownik2,
                       self.ratownik3, self.ratownik4)
        
        self.edit_fields = (self.title, self.number, self.day, self.type, self.adress,  # Fields with NO combo boxes!!!
                            self.alarm, self.arrival, self.departure, self.comeback,
                            self.combos)        

        self.injector = ValueInjector(self.dataObject)
        self.injector.populate_comboBox('czlonkowie', 'detail', self.combos)
        self.injector.fill_data("wyjazdy", 'detail', self.edit_fields, self.id)

