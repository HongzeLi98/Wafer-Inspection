from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from SelectWindow import Ui_SelectWindow
import shutil
import glob


class MySelectWindow(QDialog, Ui_SelectWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.origin_path = []
        self.restore_path = []
        self.images = []
        self.len = 0
        self.name = ''
        self.imgNum = 0
        self.direction = 0
        self.text = ['View Back', 'View Front']

        # 连接按钮和信号
        self.pushButton_Next.clicked.connect(self.on_button_next_clicked)
        self.pushButton_Previous.clicked.connect(self.on_button_previous_clicked)
        self.pushButton_Restore.clicked.connect(self.on_button_restore_clicked)
        self.pushButton_Skip.clicked.connect(self.on_button_skip_clicked)
        self.pushButton_Change.clicked.connect(self.on_button_change_clicked)

    def display(self):
        self.len = len(self.images)
        self.label_Image.setPixmap(QPixmap(self.images[self.imgNum]))
        self.label_Image.setScaledContents(True)
        self.label_Number.setText('Current:' + str(self.imgNum+1) + '/' + str(self.len) + ':Total')
        self.label_Name.setText(str(self.images[self.imgNum]))

    def on_button_change_clicked(self):
        self.pushButton_Change.setText(self.text[self.direction])
        self.direction = 1 - self.direction
        self.images = glob.glob(self.origin_path[self.direction])
        self.imgNum = 0
        self.display()

    def on_button_next_clicked(self):
        if self.imgNum < self.len-1:
            self.imgNum += 1
        else:
            self.imgNum = 0
        self.display()

    def on_button_previous_clicked(self):
        if self.imgNum == 0:
            self.imgNum = self.len - 1
        else:
            self.imgNum -= 1
        self.display()

    def on_button_skip_clicked(self):
        skip_num = int(self.lineEdit_skip.text())
        if skip_num > self.len:
            QMessageBox.warning(self, "Warning", 'Out of range!')
        else:
            self.imgNum = skip_num-1
            self.display()

    def on_button_restore_clicked(self):
        shutil.move(self.images[self.imgNum], self.restore_path[self.direction])
        self.images = glob.glob(self.origin_path[self.direction])
        self.display()




