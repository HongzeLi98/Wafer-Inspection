from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import *
from core.ScreenShot_External import shot_by_order


class CaptureThread(QThread):
    capture_signal = pyqtSignal()

    def __init__(self):
        super(CaptureThread, self).__init__()
        self.project_path = ''
        self.source_path = ''
        self.name = ''
        self.direction = 0
        self.com = ''
        self.time = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

    def run(self):
        shot_by_order(self.project_path, self.source_path, self.name, self.direction, self.com, self.x1, self.y1, self.x2, self.y2, self.time)
        self.capture_signal.emit()
