
import sys
import requests
from PyQt6 import QtWidgets as qtw, uic, QtCore
from data_model import TableModel, FetchData, ValueInjector
from colorama import Fore, init # colored prints lib

class AppState():
    def __init__(self, app=None):
        print(f"{Fore.GREEN}AppState loaded{Fore.RESET}")

        if app is None:
            app = qtw.QMainWindow
        self.app = app

        # Creating data-fetching object
        self.dataObject = FetchData("http://localhost")

        # Initializing Widgets
        self.HomePage = View_HomePage(self)
        self.Wyjazdy = View_Wyjazdy(self, self.dataObject, self.HomePage)

        # Adding widgets to stack
        self.widget_stack = qtw.QStackedWidget()
        self.widget_stack.addWidget(self.HomePage)
        self.widget_stack.addWidget(self.Wyjazdy)
        print(f"{Fore.YELLOW}Stack loaded succesfully{Fore.RESET}")


    # loading GUI page
    def loadUI(self, file: str, window: qtw.QWidget | qtw.QMainWindow, size: QtCore.QSize | None = None) -> None:

        if size == None:
            size = window.size()

        try:
            uic.loadUi(file, window)
            window.resize(size)

            if hasattr(window, "father") and window.father is not None:             # Checks if class has a parent attribute
                window.go_back.clicked.connect(lambda: self.goBack(window.father))  # if there's not parent there nowhere to go
            else:
                pass

            print(f"{Fore.GREEN}UI loaded succesfully - ({file}){Fore.RESET}")

        except Exception as e:
            print(f"{Fore.RED}loading UI Failed - ({file})\nError: {e}{Fore.RESET}")


    # loading widget
    def loadWidget(self, widget: qtw.QWidget | qtw.QMainWindow) -> None:

        self.widget_stack.setCurrentWidget(widget)

        try:
            self.app.setCentralWidget(self.widget_stack)        # Setting view to the currently active widget in stack
            print(f"{Fore.GREEN}Succesfully loaded widget - ({widget.objectName()}){Fore.RESET}")

        except Exception as e:
            print(f"{Fore.RED}Failed loading widget - ({widget})\nWith Error: {e}{Fore.RESET}")



    def goBack(self, parent: qtw.QWidget | qtw.QMainWindow):
        self.loadWidget(parent)
    

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("OSP PANEL")
        self.app_state = AppState(self)         # Connecting AppState class to a window
        self.dataObject = self.app_state.dataObject
        self.ui = "ui/login.ui"
        self.app_state.loadUI(self.ui, self, QtCore.QSize(870, 543))
        self.submit.clicked.connect(self.logIN)

    def logIN(self) -> None:
        login = self.loginField.text()
        password = self.passField.text()

        login_OK = self.dataObject.verify_user(login, password)

        if login_OK or login == '':
            self.app_state.loadWidget(self.app_state.HomePage)
        else:
            self.create_messageBox()

    def create_messageBox(self) -> None:
        print(f"{Fore.RED}Login failed. Incorret email or password{Fore.RESET}")
        # Creating a message box if login failed
        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText('Login failed')
        msg.setInformativeText("Incorrect login or passowrd")
        msg.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
        msg.exec()
        self.loginField.setText("")
        self.passField.setText("")
            

class View_HomePage(qtw.QMainWindow):
    def __init__(self, app_state: AppState, parent=None):
        super(View_HomePage, self).__init__()

        self.app_state = app_state
        self.ui = "ui/home.ui"
        self.father = parent

        self.app_state.loadUI(self.ui, self)
        self.setObjectName("HomePage")

        self.btnWyjazdy.clicked.connect(lambda: self.app_state.Wyjazdy.print_wyjazdy())
        self.btnCzlonkowie.activated.connect(self.fun)

    def fun(self):
        print("Dziala")

class View_Wyjazdy(qtw.QMainWindow):
    def __init__(self, app_state: AppState, dataObject: FetchData, parent=None):
        super(View_Wyjazdy, self).__init__()
            
        self.app_state = app_state
        self.dataObject = dataObject
        self.father = parent
        self.ui = "ui/wyjazdy.ui"
        self.detail_windows: list = []

        self.app_state.loadUI(self.ui, self)
        self.setObjectName("TestPage")

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
            self.list.doubleClicked.connect(self.showDetails)
            self.app_state.loadWidget(self.app_state.Wyjazdy)

    def showDetails(self, index) -> None:
        id = self.model.returnId(index.row())
        
        wyjazd_details = View_Wyjazd_Details(self.app_state, self.dataObject, id,)
        self.detail_windows.append(wyjazd_details)      # Pushes widget to a list of active widgets
        wyjazd_details.show()                           # makes it possible to have more than one opened



class View_Wyjazd_Details(qtw.QWidget):
    def __init__(self, app_state: AppState, dataObject: FetchData, record_id: int):
        super(View_Wyjazd_Details, self).__init__()
        self.app_state = app_state
        self.dataObject = dataObject
        self.id = record_id
        self.ui = "ui/wyjazd_details.ui"
        self.app_state.loadUI(self.ui, self, QtCore.QSize(800, 700))
        self.setWindowTitle(f"Wyjazd nr: {self.id}")
        self.closeBtn.clicked.connect(lambda: self.close())
        self.combos = (self.commander, self.driver, self.ratownik1, self.ratownik2,
                       self.ratownik3, self.ratownik4)
        
        self.edit_fields = (self.title, self.number, self.day, self.type, self.adress,  # Fields with NO combo boxes!!!
                            self.alarm, self.arrival, self.departure, self.comeback,
                            self.combos)
        

        self.injector = ValueInjector(self.dataObject)
        self.injector.populate_comboBox('czlonkowie', 'detail', self.combos)
        self.injector.fill_data("wyjazdy", 'detail', self.edit_fields, self.id)
        #self.populate_comboBox()'''

    '''
    def populate_comboBox(self) -> None:
        def listOut_values(*args) -> list:                                          # Takes out values from dict and puts
            return [[list(item.values())[0] for item in arg] for arg in args]       # bare strings into lists 

        _, table_columns = self.dataObject.fetch_table_data('czlonkowie', 'detail')
        print(f"{Fore.CYAN}{tuple(table_columns.keys())}")

        for box in self.combo_boxes.values():
            box_values = listOut_values(table_columns.get(box.objectName()))
            box.addItems(box_values)
        
        self.commanderS = members.get('commanders')
        self.driverS = members.get('drivers')
        self.czlonkowie = members.get('czlonkowie')
        self.commanderS, self.driverS =list_values(self.commanderS, self.driverS)

        self.commander.addItems(self.commanderS)
        self.driver.addItems(self.driverS)'''
        
        


def main() -> None:
    init(True)                          #initializing colorama lib
    app = qtw.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
    