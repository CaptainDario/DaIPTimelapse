#default
import sys
import os
#PySide2
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QIODevice




def load_ui_file(path : str):
    """
    Loads the main ".ui"-file from the "ui"-folder and returns the QMainWindow from it.
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


    return window

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def save_ui(ui : main_ui):
    """Writes the ui values to the file in the tempdir.

    Write the data in the following format (ui-values from top to bottom):
    #######
    name
    IP-addr
    path
    time till next image
    fps
    delete images
    #######

    Args:
        ui : the main_ui instance to read the values from.
    """

    data_file = os.path.join(tempfile.gettempdir(), about.name, about.data_file_name)
    with open(data_file, "a+") as f:
        f.write("#######\n")
        f.write(ui.lineEdit_name.text() + "\n")
        f.write(ui.lineEdit_IP_address.text() + "\n")
        f.write(ui.lineEdit_timelapse_path.text() + "\n")
        f.write(str(ui.spinBox_time_till_next_image.value()) + "\n")
        f.write(str(ui.spinBox_fps.value()) + "\n")
        f.write(str(ui.checkBox_delete_images.isChecked()) + "\n")
        f.write("#######\n")
