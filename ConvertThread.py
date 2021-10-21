from PyQt5.QtCore import QThread, pyqtSignal
from core.ConvertXML import Convert


class ConvertThread(QThread):
    convert_signal = pyqtSignal()

    def __init__(self):
        super(ConvertThread, self).__init__()
        self.project_path = ''
        self.source_path = ''


    def run(self):
        Convert(self.project_path, self.source_path)
        self.convert_signal.emit()