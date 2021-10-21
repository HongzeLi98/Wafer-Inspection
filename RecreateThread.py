from PyQt5.QtCore import QThread, pyqtSignal
from core.RecreateXML import Recreate


class RecreateThread(QThread):
    recreate_signal = pyqtSignal()

    def __init__(self):
        super(RecreateThread, self).__init__()
        self.project_path = ''
        self.source_path = ''
        self.name = ''
        self.Ok_num = 0
        self.Ng_num = 0

    def run(self):
        Recreate(self.project_path, self.source_path, self.name, self.Ok_num, self.Ng_num)
        self.recreate_signal.emit()