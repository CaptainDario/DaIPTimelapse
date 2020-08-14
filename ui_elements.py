#default
import os
import requests
import re
#PySide
from PySide2.QtWidgets import QToolButton, QMainWindow, QLabel,\
                                QPushButton, QLineEdit, QSpinBox, QFileDialog,\
                                QMessageBox
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import QByteArray, Qt, QTimer
#custom
import timelapse

url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE) 


class ui(object):
    
    lineEdit_IP_address             = None

    lineEdit_timelapse_path         = None
    toolButton_timelapse_path       = None

    lineEdit_name                   = None

    spinBox_time_till_next_image    = None

    label_video_stream              = None
    label_last_image_taken          = None

    pushButton_start_stop_timelapse = None 

    refresh_view_timer = None

    curren_timelapse = None


    def __init__(self, window : QMainWindow):

        self.window = window
        
        self.set_important_ui_elements()
        self.set_icons()
        self.connect_ui()

        #refresh camera stream every x seconds
        self.refresh_view_timer = QTimer()
        self.refresh_view_timer.setInterval(500)
        self.refresh_view_timer.timeout.connect(self.refresh_preview)
        self.refresh_view_timer.start()

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
        
        label_pixmap = QPixmap(os.path.join("img", "placeholder.png"))
        self.label_video_stream.setPixmap(label_pixmap)
        self.label_video_stream.setMask(label_pixmap.mask())
        
        label_pixmap = QPixmap(os.path.join("img", "placeholder.png"))
        self.label_last_image_taken.setPixmap(label_pixmap)
        self.label_last_image_taken.setMask(label_pixmap.mask())

    def connect_ui(self):
        self.toolButton_image_path.clicked.connect(self.set_timelapse_dir)
        self.pushButton_start_stop_timelapse.clicked.connect(self.start_timelapse)
        self.window.findChild(QPushButton, "pushButton").clicked.connect(self.refresh_preview)



    
    #Button functions
    def set_timelapse_dir(self):
        file_path = QFileDialog.getExistingDirectory(caption="Select Directory")
        print(file_path)
        self.lineEdit_timelapse_path.setText(file_path)

    def start_timelapse(self):
        """Checks if all parameter entered in the ui is valid and if so starts a timelapse.
        """

        #read textedits
        IP_addr = self.lineEdit_IP_address.text()
        path    = self.lineEdit_timelapse_path.text()
        name    = self.lineEdit_name.text()

        #check if all values are entered 
        if(IP_addr == "" or path == "" or name == ""):
            QMessageBox.critical(None, "Error", "Not all necessary parameters were set!")
        elif(os.path.exists(os.path.join(path, name))):
            msgBox = QMessageBox.critical(None, "Error", ("In the given path a folder called: '%s' already exists!" % name))
        elif(not os.path.isdir(path)):
            msgBox = QMessageBox.critical(None, "Error", ("The given path does not exists!"))
        else:
            self.current_timelapse = timelapse.timelapse(IP_addr, path, name,
                                                        self.spinBox_time_till_next_image.value(),
                                                        self.label_video_stream,
                                                        self.label_last_image_taken)


    def refresh_preview(self):
        """Downloads the current image from the given URL and previews it in the label.
        """

        print(re.match(url_regex, self.lineEdit_IP_address.text()) is not None)
        if(re.match(url_regex, self.lineEdit_IP_address.text()) is not None):

            w, h = self.label_video_stream.width(), self.label_video_stream.height()
            img = requests.get(self.lineEdit_IP_address.text(), stream=True)

            if(img.status_code == 200):
                img.raw.decode_content = True
                label_pixmap = QPixmap()
                label_pixmap.loadFromData(QByteArray(img.raw.data))
                if(label_pixmap is not None):
                    self.label_video_stream.setPixmap(label_pixmap.scaledToWidth(w))
                else:
                    print("An unexpected error appeared during image downloading/conversion!")
                    print("Please check that the IP-camera is returning a valid image and the URL is set correctly.")
                    #error during image download/conversion -> show placeholder
                    label_pixmap = QPixmap(os.path.join("img", "placeholder.png"))
                    self.label_video_stream.setPixmap(label_pixmap)
                    self.label_video_stream.setMask(label_pixmap.mask())
