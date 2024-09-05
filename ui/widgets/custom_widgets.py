
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QTimer, pyqtSignal

class DoubleClickButton(QPushButton):

    activated = pyqtSignal()

    def __init__(self, parent=None):
        super(DoubleClickButton, self).__init__(parent)
        self.counter = 0    
        self.clicked.connect(self.clickCount)

    def clickCount(self) -> None:
        self.counter += 1
        if self.counter == 1:
            self.timer = QTimer(self)
            self.timer.singleShot(700, self.checkForDoubleClick)
        elif self.counter >= 2:
            self.activated.emit()

    def checkForDoubleClick(self) -> None:
        if self.counter < 2:
            #self.activated.emit()
            print("To slow")

        self.counter = 0
 