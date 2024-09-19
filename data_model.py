
import requests
from PyQt6.QtCore import QAbstractTableModel ,Qt
from PyQt6.QtWidgets import QLineEdit, QComboBox
from colorama import Fore
from typing import Literal

class TableModel(QAbstractTableModel):
    def __init__(self, data: dict, cut_id: bool = False):
        super(TableModel, self).__init__()
        self._data = data
        self.cut_id = cut_id
        self.table = self.createTable()

    def rowCount(self, index) -> int:
        return len(self._data)
    
    def columnCount(self, index) -> int:
        if self.cut_id == False:
            return len(self._data[0])
        else:
            return len(self._data[0]) - 1
    
    def createTable(self) -> list:
        table = [list(item.values()) for item in self._data]    # Converting dict to a 2D list
        return table

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
               return self.table[index.row()][index.column()]
        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return list(self._data[0].keys())[section]
            if orientation == Qt.Orientation.Vertical:
                return section + 1
        return None
    
    def returnId(self, index: int) -> int:
        id_index = len(self._data[0]) - 1      # Always importing id as last value in a row
        return self.table[index][id_index]
    
    def refresh(self, new_data: dict) -> None:
        self.beginResetModel()
        self._data = new_data
        self.table = self.createTable()
        self.endResetModel()


class DataHandler():
    def __init__(self, base_url: str):
        self.base_url = base_url

    def connect(self, script: str, post: str | dict | None = None, no_JSON: bool = False) -> dict:
        url = f'{self.base_url}/{script}'

        response = requests.post(url, data=post) if post is not None else requests.get(url)
        return response.text if no_JSON else response.json()

    def verify_user(self, login: str, password: str) -> bool:
        script_name = "auth.php"
        post_data = {
            'login' : login,
            'password' : password
        }

        try:
            response = self.connect(script_name, post_data)

            if response['status'] == 'approved':
                return True
            else:
                return False
            
        except requests.exceptions.RequestException as e:                               #Catching exception
            self.print_connection_error(e, response['msg'])
            return False
        
    def fetch_table_data(self, table: str, mode: Literal['short', 'detail'] = 'short', id: int = -1) -> bool | dict | str:
        if mode not in ['short', 'detail']:
            raise ValueError(f"Unsupported 'mode' argument: {mode}")

        script_name = "fetch_data.php"
        post_data = {
            'table': table,
            'mode' : mode,
            'id' : id
        }
        
        try: 
            response = self.connect(script_name, post=post_data)
            
            if response['status'] == 'failed':
                print(f"{Fore.RED}Failed with Query: {response['msg']}{Fore.RESET}")
                return False, response['msg']
            else:
                return True, response['data']
        except requests.exceptions.RequestException as e:                               #Catching exception
            #self.print_connection_error(e, response['msg'])
            print(f"{Fore.RED}Error: {e}{Fore.RESET}")
            return False, "Exception"
        
    def query_db(self, section: str, data: dict, action: Literal["update", "insert", "delete"]) -> bool:

        if action == "update":
            scrtipt_name = "update_table.php"
        elif action == "insert":
            scrtipt_name = "insert.php"
        elif action == "delete":
            scrtipt_name = "delete.php"

        data['section'] = section

        try:
            response = self.connect(scrtipt_name, post=data, no_JSON=True)
            if response.strip() == "Query successfull":
                return True
            else:
                print(f"{Fore.RED}{response}{Fore.RESET}")
                return False
        except  requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Failed sending data to databse: {e}{Fore.RESET}")
            return False
        
    def print_connection_error(self, error, message: str):              # Printing connection error message
        print(f"{Fore.RED}Failed connecting to a server\nError: {error}{Fore.RESET}")
        print(message['msg'])


class ValueInjector():
    def __init__(self, dataObject: DataHandler) -> None:
        self.dataObject = dataObject

    
    def inject_values(func):
        def wrapper(self, *args, **kwargs):
            values, fields = func(self, *args, **kwargs)    # Executes decorated function fill_data

            for field in fields:                # Loops through widgets tuple and sets their values to data fetched from DB
                if isinstance(field, tuple):
                    for comboBox in field:        # If it gets to tuple of comboBoxes, it loops through this nested tuple and sets setCurrentText
                        field_value = values.get(comboBox.objectName())
                        if field_value == None:
                            item_index = 0
                        else:
                            item_index = comboBox.findText(field_value)
                            
                        comboBox.setCurrentIndex(item_index)
                else:
                    if not isinstance(field, QLineEdit):
                        raise TypeError(f"{Fore.RED}Object is not QLineEdit or QComboBox{Fore.RESET}")
                    field_value = values.get(field.objectName())    # Looks for key name corresponding to objectName in db data and assings value
                    field.setText(field_value)
                      
                
        return wrapper    
    
    @inject_values      # Decorator for injecting values ("calls both functions")
    def fill_data(self, db_table: str, mode: Literal['detail', 'short'], editFields: tuple, id: int = None) -> dict | tuple:
        '''
        Takes name of database table and puts this data into editFields widgets. ID is optional
        if function should return specified row of passed ID in database. Doesn't add items to QComboBox
        '''
        fetch_OK, table_data = self.dataObject.fetch_table_data(db_table, mode, id)   # Returns if fetch succesfull and table_data [list/dict]
        if not fetch_OK:
            print(f"{Fore.RED}Failed loading detailed data{Fore.RESET}")
            raise ValueError(f"{Fore.RED}Data couldn't be fetched{Fore.RESET}")
            
        if isinstance(table_data, list):
            table_data: dict = table_data[0]            # table_data is a one-element list returned from a function
                                                        # so we have to take out the dict from it
        return table_data, editFields
    

    def populate_comboBox(self, db_table: str, mode: Literal['detail', 'short'], comboBox: QComboBox | tuple):
        _, table_columns = self.dataObject.fetch_table_data(db_table, mode)

        def is_ratownikBox(box: QComboBox):     # In wyjazdy there are multiple combos based on 'czlonkowie' and they 
            if "ratownik" in box.objectName():  # don't have their own record so it checks for exception
                return True
            return False

        def make_list(box: QComboBox) -> list:
            rows = table_columns.get('czlonkowie' if is_ratownikBox(box) else box.objectName())     # If no ratownik[i] get correspondind key
            box_values = [list(column.values())[0] for column in rows]  # makes list from key-values of a few one-element lists
            return box_values
        
        def insert_items(box: QComboBox):
            box_values = make_list(box)
            if box.accessibleName() == "nullable":          # Adds 'Brak' item if corresponding db column is nullable
                box.addItem("Brak", 0)
            for value in box_values:                        # make_list returns list of 'value, value_id' so
                if "," in value:
                    split_id: list = value.split(',')           # this splits this string in list of [value, value_id]
                    value_text = split_id[0]                    # and inserts to QComboBox value and 'user_data' as value_id
                    value_id = int(split_id[1].strip())
                    box.addItem(value_text, userData=value_id)
                else:
                    box.addItem(value)

        if isinstance(comboBox, tuple):
            for box in comboBox:
                insert_items(box)
        elif isinstance(comboBox, QComboBox):
            insert_items(comboBox)
