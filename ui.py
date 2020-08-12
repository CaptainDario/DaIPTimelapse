#default
import os, sys
#PySide2
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QIODevice
from PySide2.QtGui import QIcon
#custom
import ui_elements


ui = None



def start_timelapse():

    if(os.path.exists(image_location)):
        project_name = "project_name"
        os.chdir(image_location)
        # check if there is no folder with the given name
        if(os.path.exists(os.path.join(image_location, project_name))):
            os.mkdir(project_name)
            os.chdir(project_name)
            os.mkdir(project_name + "images")
        else:
            print("A folder with the given project name already exists!")
    else:
        print("path does not exists")


def load_ui_file(path : str):
    """Loads the main ".ui"-file from the "ui"-folder and returns the QMainWindow from it.
    Also initializes an instance of the "ui"-class.

    Arguments:
        path : the path to the ui file which should be loaded

    Returns:
        QWindow: The loaded Window

    """
    
    ui_file = QFile(path)

    if not ui_file.open(QIODevice.ReadOnly):
        print("Cannot open {}: {}".format(path, ui_file.errorString()))
        sys.exit(-1)

    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()

    if not window:
        print(loader.errorString())
        sys.exit(-1)

    global ui
    ui = ui_elements.ui(window)

    return window