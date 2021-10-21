from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from MainWindow import Ui_MainWindow
import glob
import os
import sys
import MyDialog
import MySelectWindow
import CaptureThread
import InspectThread
import ConvertThread
import RecreateThread


class DemoMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # 调用Ui_Mainwindow中的函数setupUi实现显示界面
        self.setupUi(self)
        # 定义New project对话框
        self.new_dialog = MyDialog.MyDialog()
        self.new_dialog.choose_signal.connect(self.choose_dir)
        # 定义选择图片的对话框
        self.new_select = MySelectWindow.MySelectWindow()
        # 定义项目路径
        self.project_path = ''
        # 定义各个线程
        self.mCaptureThread = CaptureThread.CaptureThread()
        self.mInspectThread = InspectThread.InspectThread()
        self.mConvertThread = ConvertThread.ConvertThread()
        self.mRecreateThread = RecreateThread.RecreateThread()
        # 连接按钮和信号
        self.pushButton_NewProject.clicked.connect(self.new_dialog.show)
        self.pushButton_OpenProject.clicked.connect(self.on_button_open_clicked)
        self.pushButton_Select.clicked.connect(self.on_button_select_clicked)
        self.pushButton_CaptureBack.clicked.connect(self.on_button_capture_back_clicked)
        self.pushButton_CaptureFront.clicked.connect(self.on_button_capture_front_clicked)
        self.pushButton_Inspect.clicked.connect(self.on_button_inspect_clicked)
        # 连接信号和回调函数
        self.mCaptureThread.capture_signal.connect(self.capture_callback)
        self.mInspectThread.inspect_signal.connect(self.inspect_callback)
        self.mConvertThread.convert_signal.conndct(self.convert_callback)
        self.mRecreateThread.recreate_signal.connect(self.recreate_callback)


    # 打开项目之后，设定项目路径
    def choose_dir(self, s):
        self.statusbar.showMessage(s)
        self.project_path = s
        os.mkdir(self.project_path)
        os.mkdir(self.project_path + '/Input/')
        os.mkdir(self.project_path + '/Input/Back/')
        os.mkdir(self.project_path + '/Input/Front/')
        os.mkdir(self.project_path + '/Input/Manual_XML/')
        os.mkdir(self.project_path + '/Output/')
        os.mkdir(self.project_path + '/Output/Back/')
        os.mkdir(self.project_path + '/Output/Back/NG/')
        os.mkdir(self.project_path + '/Output/Back/OK/')
        os.mkdir(self.project_path + '/Output/Back/Xml/')
        os.mkdir(self.project_path + '/Output/Front/')
        os.mkdir(self.project_path + '/Output/Front/NG/')
        os.mkdir(self.project_path + '/Output/Front/OK/')
        os.mkdir(self.project_path + '/Output/Front/Xml/')
        os.mkdir(self.project_path + '/Output/Xml/')

    def on_button_open_clicked(self):
        s = QFileDialog.getExistingDirectory(self)
        self.statusbar.showMessage(s)
        self.project_path = s

    def on_button_select_clicked(self):
        if self.project_path == '':
            QMessageBox.warning(self, "Warning", 'Please choose your project path!')
        else:
            self.new_select.restore_path = [self.project_path + '/Output/Back/OK/', self.project_path + '/Output/Front/OK/']
            self.new_select.origin_path = [self.project_path + '/Output/Back/NG/*.jpg', self.project_path + '/Output/Front/NG/*.jpg']
            self.new_select.images = glob.glob(self.new_select.origin_path[0])
            self.new_select.show()
            self.new_select.display()

    def on_button_capture_back_clicked(self):
        self.mCaptureThread.project_path = self.project_path
        self.mCaptureThread.source_path = ''
        self.mCaptureThread.name = self.lineEdit_Name.text() + '_B'
        self.mCaptureThread.direction = 0
        self.mCaptureThread.com = self.lineEdit_COM
        self.mCaptureThread.time = float(self.lineEdit_Time.text())
        self.mCaptureThread.x1 = int(self.lineEdit_X1.text())
        self.mCaptureThread.y1 = int(self.lineEdit_Y1.text())
        self.mCaptureThread.x2 = int(self.lineEdit_X2.text())
        self.mCaptureThread.y2 = int(self.lineEdit_Y2.text())
        self.mCaptureThread.start()

    def on_button_capture_front_clicked(self):
        self.mCaptureThread.project_path = self.project_path
        self.mCaptureThread.source_path = './Source/'
        self.mCaptureThread.name = self.lineEdit_Name.text() + '_F'
        self.mCaptureThread.direction = 1
        self.mCaptureThread.com = self.lineEdit_COM
        self.mCaptureThread.time = float(self.lineEdit_Time.text())
        self.mCaptureThread.x1 = int(self.lineEdit_X1.text())
        self.mCaptureThread.y1 = int(self.lineEdit_Y1.text())
        self.mCaptureThread.x2 = int(self.lineEdit_X2.text())
        self.mCaptureThread.y2 = int(self.lineEdit_Y2.text())
        self.pushButton_CaptureBack.setEnabled(False)
        self.pushButton_CaptureFront.setEnabled(False)
        self.pushButton_Inspect.setEnabled(False)
        self.mCaptureThread.start()

    def capture_callback(self):
        QMessageBox.information(self, "Info", 'Images collection completed!')
        self.pushButton_CaptureBack.setEnabled(True)
        self.pushButton_CaptureFront.setEnabled(True)
        self.pushButton_Inspect.setEnabled(True)

    def on_button_inspect_clicked(self):
        self.mInspectThread.project_path = self.project_path
        self.mInspectThread.source_path = './Source/'
        self.mInspectThread.name = self.lineEdit_Name.text()
        self.mInspectThread.Ok_num = int(self.lineEdit_OK.text())
        self.mInspectThread.Ng_num = int(self.lineEdit_NG.text())
        self.pushButton_CaptureBack.setEnabled(False)
        self.pushButton_CaptureFront.setEnabled(False)
        self.pushButton_Inspect.setEnabled(False)
        self.mInspectThread.start()

    def inspect_callback(self):
        QMessageBox.information(self, "Info", 'Inspection completed!')
        self.pushButton_CaptureBack.setEnabled(True)
        self.pushButton_CaptureFront.setEnabled(True)
        self.pushButton_Inspect.setEnabled(True)

    def on_button_convert_clicked(self):
        self.mConvertThread.project_path = self.project_path
        self.mConvertThread.source_path = './Source/'
        self.pushButton_Convert.setEnabled(False)
        self.mConvertThread.start()

    def convert_callback(self):
        QMessageBox.information(self, "Info", 'Convert Successfully!')
        self.pushButton_Convert.setEnabled(True)

    def on_button_recreate_clicked(self):
        self.mRecreateThread.project_path = self.project_path
        self.mRecreateThread.source_path = './Source/'
        self.mRecreateThread.name = self.lineEdit_Name.text()
        self.mRecreateThread.Ok_num = int(self.lineEdit_OK.text())
        self.mRecreateThread.Ng_num = int(self.lineEdit_NG.text())
        self.pushButton_Recreate.setEnabled(False)
        self.mRecreateThread.start()

    def recreate_callback(self):
        QMessageBox.information(self, "Info", 'Recreate Successfully!')
        self.pushButton_Recreate.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DemoMain()
    demo.setWindowTitle('GATD Application')
    demo.show()
    sys.exit(app.exec_())
