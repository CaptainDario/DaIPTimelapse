#default
import os
import re
#PySide
from PySide2.QtWidgets import QCheckBox, QToolButton, QMainWindow, QLabel,\
                                QPushButton, QLineEdit, QSpinBox, QFileDialog,\
                                QMessageBox
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import QByteArray, Qt, QTimer
#custom
import timelapse
import network
import IO



class main_ui(object):
    
    lineEdit_IP_address             = None

    lineEdit_timelapse_path         = None
    toolButton_timelapse_path       = None

    lineEdit_name                   = None

    spinBox_time_till_next_image    = None
    spinBox_fps                     = None

    pushButton_start_timelapse      = None 
    checkBox_delete_images          = None

    window_stream_preview           = None

    #an array of all timelapses which are currently running
    current_timelapses = []


    def __init__(self, window : QMainWindow):

        self.window = window
        
        self.set_important_ui_elements()
        self.set_icons()
        self.connect_ui()


    def set_important_ui_elements(self):
        '''
        Set the references to the ui elements read from the .ui file
        '''
        self.lineEdit_IP_address          = self.window.findChild(QLineEdit,   "lineEdit_IP_address")

        self.lineEdit_timelapse_path      = self.window.findChild(QLineEdit,   "lineEdit_timelapse_path")
        self.toolButton_image_path        = self.window.findChild(QToolButton, "toolButton_timelapse_path")

        self.lineEdit_name                = self.window.findChild(QLineEdit,   "lineEdit_name")
        
        self.spinBox_time_till_next_image = self.window.findChild(QSpinBox,    "spinBox_time_till_next_image")
        self.spinBox_fps                  = self.window.findChild(QSpinBox,    "spinBox_fps")

        self.checkBox_delete_images       = self.window.findChild(QCheckBox,   "checkBox_delete_images")
        self.pushButton_start_timelapse   = self.window.findChild(QPushButton, "pushButton_start_timelapse")

    def set_icons(self):
        self.toolButton_image_path.setIcon(QIcon("img/folder_black.png"))
        

    def connect_ui(self):
        '''
        Connect the ui with their functions
        '''
        self.toolButton_image_path.clicked.connect(self.set_timelapse_dir)
        self.pushButton_start_timelapse.clicked.connect(self.start_timelapse)
        self.window.findChild(QPushButton, "pushButton_preview").clicked.connect(self.show_ip_preview)

    
    #--- Button functions ----
    def set_timelapse_dir(self):
        '''
        Open a file dialog to set the directory where to save the timelapse videos/image.
        '''
        file_path = QFileDialog.getExistingDirectory(caption="Select Directory")
        print(file_path)
        self.lineEdit_timelapse_path.setText(file_path)

    def start_timelapse(self):
        """
        Checks if all parameter entered in the ui are valid and if so starts a timelapse.
        """

        #read textedits
        IP_addr = self.lineEdit_IP_address.text()
        path    = self.lineEdit_timelapse_path.text()
        name    = self.lineEdit_name.text()
        spf     = self.spinBox_time_till_next_image.value()
        fps     = self.spinBox_fps.value()
        del_img = self.checkBox_delete_images.isChecked()

        #check if all values are entered 
        if(IP_addr == "" or path == "" or name == ""):
            QMessageBox.critical(None, "Error", "Not all necessary parameters were set!")
        elif(os.path.exists(os.path.join(path, name))):
            msgBox = QMessageBox.critical(None, "Error", ("In the given path a folder called: '%s' already exists!" % name))
        elif(not os.path.isdir(path)):
            msgBox = QMessageBox.critical(None, "Error", ("The given path does not exists!"))
        else:
            self.current_timelapses.append(timelapse.timelapse(IP_addr, path, name,
                                            spf, fps, del_img))

    def show_ip_preview(self):
        '''
        Opens a new window and shows a preview of the camera stream.
        '''
        
        self.window_stream_preview = IO.load_ui_file(os.path.join("ui", "stream_preview.ui")) 
        self.window_stream_preview.show()
        self.window_stream_preview.setWindowTitle("IP Preview")
        valid = network.check_camera_ip(self.lineEdit_IP_address.text(),
                                self.window_stream_preview.label_video_stream_preview)
        if(not valid):
            self.window_stream_preview.close()
            QMessageBox.critical(None, "Error", ("An unexpected error appeared during image downloading/conversion! \n" + \
                                        "Please check that the IP-camera is returning a valid image and the URL is set correctly."))

