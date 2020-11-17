#default
import os
from functools import partial
#PySide
from PySide2.QtWidgets import QCheckBox, QMenu, QToolButton, QMainWindow, \
                                QPushButton, QLineEdit, QSpinBox, QFileDialog,\
                                QMessageBox
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
#custom
import timelapse
import network
import IO



class main_ui(object):
    """The main-UI of the IP-time-lapse-toll.

    Attributes:
        menuFile                           (QMenu) : The menu with the items to save and load configs.
        lineEdit_IP_address            (QLineEdit) : The LineEdit in which the user can enter the ip address of the IP-Camera.
        lineEdit_timelapse_path        (QLineEdit) : LineEdit for the path to the timelapse.
        toolButton_timelapse_path    (QToolButton) : ToolButton to select the path for the timelapse with a file dialog.
        lineEdit_name                  (QLineEdit) : LineEdit to give the TimeLapse a name.
        spinBox_time_till_next_image    (QSpinBox) : SpinBox to set the time when a new image from the ip stream should be grabbed.
        spinBox_fps                     (QSpinBox) : SpinBox to set the target fps of the rendered video.
        pushButton_start_timelapse   (QPushButton) : Button to start a timelapse with the given parameters.
        checkBox_delete_images         (QCheckBox) : CheckBox If the images should be delted after a time lapse was rendered.
        window_stream_preview             (QLabel) : The window which previews the IP camera stream.
        current_timelapses           ([timelapse]) : List of the running timelapse(s).
    """
    
    menuFile                        = None

    lineEdit_IP_address             = None

    lineEdit_timelapse_path         = None
    toolButton_timelapse_path       = None

    lineEdit_name                   = None

    spinBox_time_till_next_image    = None
    spinBox_fps                     = None

    pushButton_start_timelapse      = None 
    checkBox_delete_images          = None

    window_stream_preview           = None

    current_timelapses = []
    loaded_configs     = []


    def __init__(self, window : QMainWindow):

        self.window = window
        print(os.getcwd())
        window.setWindowIcon(QIcon(IO.resource_path("img/icon.ico")))
        
        self.set_important_ui_elements()
        self.set_icons()
        self.connect_ui()
        #load the saved configurations and add them to the menubar
        self.create_menu()


    def set_important_ui_elements(self):
        '''
        Set the references to the ui elements read from the .ui file
        '''

        self.menuFile                     = self.window.findChild(QMenu, "menuFile")

        self.lineEdit_IP_address          = self.window.findChild(QLineEdit,   "lineEdit_IP_address")

        self.lineEdit_timelapse_path      = self.window.findChild(QLineEdit,   "lineEdit_timelapse_path")
        self.toolButton_image_path        = self.window.findChild(QToolButton, "toolButton_timelapse_path")

        self.lineEdit_name                = self.window.findChild(QLineEdit,   "lineEdit_name")
        
        self.spinBox_time_till_next_image = self.window.findChild(QSpinBox,    "spinBox_time_till_next_image")
        self.spinBox_fps                  = self.window.findChild(QSpinBox,    "spinBox_fps")

        self.checkBox_delete_images       = self.window.findChild(QCheckBox,   "checkBox_delete_images")
        self.pushButton_start_timelapse   = self.window.findChild(QPushButton, "pushButton_start_timelapse")

    def set_icons(self):
        self.toolButton_image_path.setIcon(QIcon(IO.resource_path(os.path.join("img", "folder_black.png"))))


    def create_menu(self):
        """Adds all QActions to the file menu from the menubar.
        """

        self.loaded_configs = IO.load_time_lapse_configs()
        self.menuFile.clear()

        #add the load and delete sub-menu
        sub_load = self.menuFile.addMenu("Load config")
        sub_del  = self.menuFile.addMenu("Delete config")

        #load the stored configs and append them to the sub-menus
        for c, name in enumerate(self.loaded_configs):
            load_entry = sub_load.addAction(name[0])
            load_entry.triggered.connect(partial(self.set_loaded_ui_values, name))

            del_entry  = sub_del.addAction(name[0])
            del_entry.triggered.connect(partial(IO.delete_config, self.loaded_configs, c))
            del_entry.triggered.connect(self.create_menu)

        #add the reload and save action
        self.menuFile.addSeparator()
        save   = self.menuFile.addAction("Save current config")
        reload = self.menuFile.addAction("Reload configs")
        
        #connect the actions
        save.triggered.connect(lambda : IO.save_ui(self.window.lineEdit_name.text(),
                                                    self.window.lineEdit_IP_address.text(),
                                                    self.window.lineEdit_timelapse_path.text(),
                                                    str(self.window.spinBox_time_till_next_image.value()),
                                                    str(self.window.spinBox_fps.value()),
                                                    str(self.window.checkBox_delete_images.isChecked())))
        save.triggered.connect(self.create_menu)
        reload.triggered.connect(self.create_menu)

    def connect_ui(self):
        '''
        Connect the ui with their functions
        '''
        self.toolButton_image_path.clicked.connect(self.set_timelapse_dir)
        self.pushButton_start_timelapse.clicked.connect(self.start_timelapse)
        self.window.pushButton_preview.clicked.connect(self.show_ip_preview)

    def set_loaded_ui_values(self, ui_values : list[str]):
        """Sets the ui according to the given list of ui values.

        Note:
            The ui_values param is expected to be one of the arrays of the array
            of values of IO.load_time_lapse_config

        Args:
            ui_values (list[str]): A list of ui values which will define the new UI states
        """

        self.window.lineEdit_name.setText(ui_values[0])
        self.window.lineEdit_IP_address.setText(ui_values[1])
        self.window.lineEdit_timelapse_path.setText(ui_values[2])
        self.window.spinBox_time_till_next_image.setValue(int(ui_values[3]))
        self.window.spinBox_fps.setValue(int(ui_values[4]))
        self.window.checkBox_delete_images.setCheckState(Qt.CheckState(ui_values[5] == "True"))

    
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
            msgb = QMessageBox(QMessageBox.Critical,
                                "Error",
                                "Not all necessary parameters were set!",
                           buttons=QMessageBox.Ok)
            msgb.setWindowIcon(QIcon(IO.resource_path("img/icon.ico")))
            msgb.exec()
        elif(os.path.exists(os.path.join(path, name))):
            msgb = QMessageBox(QMessageBox.Critical,
                                "Error",
                                ("In the given path a folder called: '%s' already exists!" % name),
                           buttons=QMessageBox.Ok)
            msgb.setWindowIcon(QIcon(IO.resource_path("img/icon.ico")))
            msgb.exec()
        #check if path is valid
        elif(not os.path.isdir(path)):
            msgb = QMessageBox(QMessageBox.Critical,
                                "Error",
                                ("The given path does not exists!"),
                           buttons=QMessageBox.Ok)
            msgb.setWindowIcon(QIcon(IO.resource_path("img/icon.ico")))
            msgb.exec()
        #check if an image can be downloaded from the IP address
        elif(not network.check_camera_ip(IP_addr)):
            msgb = QMessageBox(QMessageBox.Critical,
                                "Error",
                                "An unexpected error appeared during image downloading and conversion! \n" + \
                                "Please check that the IP-camera is returning a valid image and the URL is set correctly.",
                           buttons=QMessageBox.Ok)
            msgb.setWindowIcon(QIcon(IO.resource_path("img/icon.ico")))
            msgb.exec()
        else:
            tl = timelapse.timelapse(IP_addr, path, name, spf, fps, del_img)
            self.current_timelapses.append(tl)

    def show_ip_preview(self):
        '''
        Opens a new window and shows a preview of the camera stream.
        '''
        
        self.window_stream_preview = IO.load_ui_file(IO.resource_path(os.path.join("ui", "stream_preview.ui")))
        self.window_stream_preview.show()
        self.window_stream_preview.setWindowTitle("IP Preview")
        self.window_stream_preview.setWindowIcon(QIcon(IO.resource_path("img/icon.ico")))
        valid = network.check_camera_ip_ui(self.lineEdit_IP_address.text(),
                                self.window_stream_preview.label_video_stream_preview)
        if(not valid):
            self.window_stream_preview.close()
            msgb = QMessageBox(QMessageBox.Critical,
                                "Error",
                                "An unexpected error appeared during image downloading and conversion! \n" + \
                                "Please check that the IP-camera is returning a valid image and the URL is set correctly.",
                           buttons=QMessageBox.Ok)
            msgb.setWindowIcon(QIcon(IO.resource_path("img/icon.ico")))
            msgb.exec()
