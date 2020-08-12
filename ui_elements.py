#default
import os
import requests
#PySide
from PySide2.QtWidgets import QToolButton, QMainWindow, QLabel,\
                                QPushButton, QLineEdit, QSpinBox, QFileDialog,\
                                QErrorMessage
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import QByteArray, Qt
#custom
import timelapse



class ui(object):
    
    lineEdit_IP_address             = None

    lineEdit_timelapse_path         = None
    toolButton_timelapse_path       = None

    lineEdit_name                   = None

    spinBox_time_till_next_image    = None

    label_video_stream              = None
    label_last_image_taken          = None

    pushButton_start_stop_timelapse = None 



    def __init__(self, window : QMainWindow):

        self.window = window
        
        self.set_important_ui_elements()
        self.set_icons()
        self.connect_ui()

    def set_important_ui_elements(self):
        self.lineEdit_IP_address          = self.window.findChild(QLineEdit, "lineEdit_IP_address")

        self.lineEdit_timelapse_path      = self.window.findChild(QLineEdit,   "lineEdit_timelapse_path")
        self.toolButton_image_path        = self.window.findChild(QToolButton, "toolButton_timelapse_path")

        self.lineEdit_name                = self.window.findChild(QLineEdit,   "lineEdit_name")
        
        self.spinBox_time_till_next_image = self.window.findChild(QSpinBox,    "spinBox_time_till_next_image")

        self.label_video_stream           = self.window.findChild(QLabel,      "label_video_stream")
        self.label_last_image_taken       = self.window.findChild(QLabel,      "label_last_image_taken")

        self.pushButton_start_stop_timelapse   = self.window.findChild(QPushButton, "pushButton_start_stop_timelapse")

    def set_icons(self):
        self.toolButton_image_path.setIcon(QIcon("img/folder_black.png"))

    def connect_ui(self):
        self.toolButton_image_path.clicked.connect(self.set_timelapse_dir)
        self.pushButton_start_stop_timelapse.clicked.connect(self.start_timelapse)

    
    #Button functions
    def set_timelapse_dir(self):
        file_path = QFileDialog.getExistingDirectory(caption="Select Directory")
        print(file_path)
        self.lineEdit_timelapse_path.setText(file_path)

    def start_timelapse(self):
        timelapse.timelapse(self.lineEdit_IP_address.text(),
                            self.lineEdit_timelapse_path.text(),
                            self.lineEdit_name.text(),
                            self.spinBox_time_till_next_image.value())

