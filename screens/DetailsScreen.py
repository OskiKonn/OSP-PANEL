from data_model import ValueInjector
from PyQt6.QtWidgets import QWidget, QLineEdit, QMessageBox
from PyQt6.QtCore import QSize

class DetailsScreen(QWidget):
    def __init__(self, appState, record_id: int | None = None, empty: bool = False):
        super(DetailsScreen, self).__init__()
        self.app_state = appState
        self.dataObject = self.app_state.dataObject
        self.empty = empty
        self.ui = "ui/wyjazd_details.ui"
        self.app_state.loadUI(self.ui, self, QSize(800, 700))
        self.closeBtn.clicked.connect(self.check_for_unsaved_changes)
        self.saveBtn.clicked.connect(lambda: self.save())
        self.combos = (self.commander, self.driver, self.ratownik1, self.ratownik2,
                       self.ratownik3, self.ratownik4)
        
        self.edit_fields = (self.title, self.number, self.day, self.type, self.adress,  # Fields with NO combo boxes!!!
                            self.alarm, self.arrival, self.departure, self.comeback,
                            self.combos)        

        self.injector = ValueInjector(self.dataObject)
        self.injector.populate_comboBox('czlonkowie', 'detail', self.combos)
        self.initial_values: dict = self.get_current_values()

        if not self.empty:
            self.id = int(record_id)
            self.setWindowTitle(f"Wyjazd nr: {self.id}")
            self.injector.fill_data("wyjazdy", 'detail', self.edit_fields, self.id)

    # Catchinig current values from editable widgets
    def get_current_values(self) -> dict:
        current_data: dict = {'id' : self.id} if not self.empty else {}
        print(current_data)
        # Loop for catching current data from QLineEdits
        for field in self.edit_fields:
            if isinstance(field, QLineEdit):
                current_data[field.objectName()] = field.text()

        # Loop for catchig current data from QComboBoxes
        for comboBox in self.combos:
            item_index = comboBox.findText(comboBox.currentText())
            item_id = comboBox.itemData(item_index)
            current_data[comboBox.objectName()] = item_id

        return current_data
    
    def check_for_unsaved_changes(self) -> None:
        current_values = self.get_current_values()
        print(current_values)
        unsaved: bool = not (current_values == self.initial_values)
        if not unsaved:
            self.close()
        else:
            confirmation = self.confirm_changes()
            if confirmation == "Yes":
                self.save(current_values)
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
        
    def save(self, current_values: dict | None = None) -> None:
        if current_values == None:
            current_values = self.get_current_values()
        current_values['id'] = self.id     # self.id returned previously by PyQt6 index system is a string somehow
        update: bool = self.dataObject.send_to_db("wyjazdy", current_values)
        if update:
            print("Update succesfull")
            current_values.pop('section')           # pops 'section' key added in data_model.send_to_db
            self.initial_values = current_values    # to ensure proper get_current_values functionality
        else:
            print("Update failed")

    # Overriding closeEvent method
    def closeEvent(self, event):
        if event.spontaneous():     # Checks if user tries to exit by pressing X button
            answer = QMessageBox.question(self, "Confirm Exit", "Are you sure you want to quit? Every unsaved changes will be discarded",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            
            if answer == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
