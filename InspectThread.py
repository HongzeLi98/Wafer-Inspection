from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import *
from core.main import start_wafer


class InspectThread(QThread):
    inspect_signal = pyqtSignal()

    def __init__(self):
        super(InspectThread, self).__init__()
        self.project_path = ''
        self.source_path = ''
        self.name = ''
        self.Ok_num = 0
        self.Ng_num = 0

    def run(self):
        start_wafer(self.project_path, self.source_path, self.name, self.Ok_num, self.Ng_num)
        self.inspect_signal.emit()
