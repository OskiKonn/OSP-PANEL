from data_model import ValueInjector
from PyQt6.QtWidgets import QWidget, QLineEdit, QMessageBox
from PyQt6.QtCore import QSize

class DetailsScreen(QWidget):
    def __init__(self, app, parent, record_id: int | None = None, empty: bool = False, dbTable: str | None = None):
        super(DetailsScreen, self).__init__()
        self.app = app
        self.parent = parent
        self.dataObject = self.app.dataObject
        self.empty = empty
        self.injector = ValueInjector(self.dataObject)
        self.app.loadUI(self.ui, self, QSize(800, 700))    
        self.closeBtn.clicked.connect(self.check_for_unsaved_changes)
        self.saveBtn.clicked.connect(lambda: self.save())

        if dbTable is not None:
            self.dbTable = dbTable

        if self.empty:
            self.saveBtn.setText("Dodaj")

    # Connecting slots for enabling save button 
    def connect_slots(self) -> None:
        for box in self.combos:
            box.currentIndexChanged.connect(self.enable_saveBtn)
        
        for field in self.text_fields:
            field.textEdited.connect(self.enable_saveBtn)

    # Catchinig current values from editable widgets
    def get_current_values(self) -> dict:
        current_data: dict = {'id' : self.id} if not self.empty else {}
        # Loop for catching current data from QLineEdits
        for field in self.text_fields:
            if isinstance(field, QLineEdit):
                if field.text() == "Brak":
                  current_data[field.objectName()] = 'NULL'
                else:  
                    current_data[field.objectName()] = field.text()

        # Loop for catchig current data from QComboBoxes
        for comboBox in self.combos:
            item_index = comboBox.currentIndex()
            item_id = comboBox.itemData(item_index)
            if item_index != -1 and item_id == 0:
                current_data[comboBox.objectName()] = 'NULL'
            elif item_index != -1 and item_id != 0:
                current_data[comboBox.objectName()] = item_id
            else:
                current_data[comboBox.objectName()] = comboBox.currentText()

        return current_data
    
    def check_for_unsaved_changes(self) -> None:
        current_values = self.get_current_values()
        unsaved: bool = not (current_values == self.initial_values)
        if not unsaved:
            self.close()
        else:
            confirmation = self.confirm_changes()
            if confirmation == "Yes":
                self.save(current_values)
                #self.close()
            elif confirmation == "No":
                self.close()
    
    def confirm_changes(self) -> str:
        box = QMessageBox.warning(self, "Unsaved changes", "You have unsaved changes\n\nDo you want to keep them?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                                    QMessageBox.StandardButton.Yes)

        if box == QMessageBox.StandardButton.Yes:
            return "Yes"
        elif box == QMessageBox.StandardButton.No:
            return "No"
        else:
            return "Cancel"
        
    # Default function for saving data to DB
    def save(self, current_values: dict | None = None) -> None:
        if current_values == None:
            current_values = self.get_current_values()

        if hasattr(self, "id"):
            current_values['id'] = self.id     # self.id returned previously by PyQt6 index system is a string somehow

        saved: bool = self.dataObject.query_db(self.dbTable, current_values, "update")

        if saved:
            current_values.pop('section')           # pops 'section' key added in data_model.query_to_db
            self.disable_saveBtn()
            self.initial_values = current_values    # to ensure proper get_current_values functionality
            self.refresh_data_model()

    # Overriding closeEvent method
    def closeEvent(self, event):
        if event.spontaneous():     # Checks if user tries to exit by pressing X button
            answer = QMessageBox.question(self, "Confirm Exit", "Are you sure you want to quit? Every unsaved changes will be discarded",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            
            if answer == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()

    def refresh_data_model(self) -> None:
        _, new_data = self.dataObject.fetch_table_data(self.dbTable)
        self.parent.model.refresh(new_data)

    def enable_saveBtn(self) -> None:
        if not self.saveBtn.isEnabled():
            self.saveBtn.setEnabled(True)
            self.saveBtn.setStyleSheet("background:red")
    
    def disable_saveBtn(self) -> None:
        self.saveBtn.setEnabled(False)
        self.saveBtn.setStyleSheet("background: #bd979a")

class DetailsWyjazdy(DetailsScreen):
    def __init__(self, appState, parent, record_id: int | None = None, empty: bool = False):
        self.ui = "ui/wyjazd_details.ui"
        super().__init__(appState, parent, record_id, empty)
        self.combos = (self.commander, self.driver, self.ratownik1, self.ratownik2,
                       self.ratownik3, self.ratownik4)
        
        self.text_fields = (self.title, self.number, self.day, self.type, self.adress,  # Fields with NO combo boxes!!!
                            self.alarm, self.arrival, self.departure, self.comeback)
        
        self.injector.populate_comboBox('czlonkowie', 'detail', self.combos)
        
        if not self.empty:
            self.id = int(record_id)
            self.injector.fill_data("wyjazdy", 'detail', self.text_fields, self.combos, self.id)
            self.setWindowTitle(f"Wyjazd nr: {self.number.text()}")

        self.initial_values: dict = self.get_current_values()
        self.connect_slots()

    def unique_fighters(self) -> bool:
        '''People cannot duplicate so a fighter can be assigned to only one role in single wyjazd.
           This checks if fighetr is not assigned to multiple roles'''
        fighters: list[int] = []
        for fighter in self.combos:
            fighter_id = fighter.itemData(fighter.currentIndex())
            if fighter_id in fighters:
                return False
            else:
                fighters.append(fighter_id)

        return True

    # Overriding defaul save function in DetailsScreen class
    def save(self, current_values: dict | None = None) -> None:
        if not self.unique_fighters():
            msg = "Jeden lub więcej ratowników jest przypisany do różnych ról\n\nDokonaj niezbędnych zmian i kontynuuj"
            box = QMessageBox.information(self, "Duplikowanie ratowników", msg, QMessageBox.StandardButton.Ok)
        else:
            if current_values == None:
                current_values = self.get_current_values()

            if hasattr(self, "id"):
                current_values['id'] = self.id     

            if not self.empty:
                saved: bool = self.dataObject.query_db("wyjazdy", current_values, "update")
            else:
                saved: bool = self.dataObject.query_db("wyjazdy", current_values, "insert")

            if saved:
                current_values.pop('section')
                self.disable_saveBtn()           
                self.initial_values = current_values
                self.refresh_data_model()
                
                if self.empty : self.close()

    def refresh_data_model(self) -> None:
        _, new_data = self.dataObject.fetch_table_data("wyjazdy")
        self.parent.model.refresh(new_data)
