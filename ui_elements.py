#PySide
from PySide2.QtWidgets import QToolButton, QMainWindow
from PySide2.QtGui import QIcon


class ui(object):
    
    toolButton_image_path = None
    label_video_stream    = None 

    def __init__(self, window : QMainWindow):

        self.window = window
        self.toolButton_image_path = window.findChild(QToolButton, "toolButton_image_path")
        self.label_video_stream = window.findChild(QLabel, "label_video_stream")

        self.set_icons()

        self.connect_ui()

    def set_icons(self):
        self.toolButton_image_path.setIcon(QIcon("img/folder_black.png"))

    def connect_ui(self):
        self.toolButton_image_path.clicked.connect(lambda x : print(x))

