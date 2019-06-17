import sys
from PyQt5.QtWidgets import QDialog, QApplication
from base import *


class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.ButtonClickMe.clicked.connect(self.dispmessage)
        self.show()

    def dispmessage(self):
        self.ui.label.setText(
            ("Hello " if str(self.ui.lineEditName.text()) != "" else "No Name Entered")
            + self.ui.lineEditName.text()
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
