from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from Dialog import Ui_Dialog


class MyDialog(QDialog, Ui_Dialog):
    choose_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.path = None
        self.name = None

        # 连接按钮和信号
        self.pushButton_Choose.clicked.connect(self.on_button_choose_clicked)
        self.buttonBox.accepted.connect(self.on_button_ok_clicked)
        self.buttonBox.rejected.connect(self.on_button_cancel_clicked)

    def on_button_choose_clicked(self):
        self.path = QFileDialog.getExistingDirectory(self)
        self.lineEdit_Choose.setText(self.path)

    def on_button_ok_clicked(self):
        self.name = self.lineEdit_Name.text()
        self.path = self.path + '/' + self.name
        self.choose_signal.emit(str(self.path))
        self.path = None
        self.name = None
        self.close()

    def on_button_cancel_clicked(self):
        self.close()
