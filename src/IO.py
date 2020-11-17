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
def create_data_file():
    """Creates a file to store the UI-data in the temp-dir of the OS.

    First checks if a temp-folder already exists.
    If this is not the case a directory will be created with a file in it.
    Otherwise checks if a "data.txt" exists in the directory and creates it
    id necessary.
    """

    tempdir   = tempfile.gettempdir()
    data_dir  = os.path.join(tempdir, about.name)

    #check if the directory does not exists and create it if necessary
    if(not os.path.exists(data_dir)):
        os.makedirs(data_dir)
    
    data_file = os.path.join(data_dir, about.data_file_name)
    
    #check if the directory does not exists and create it if necessary
    if(not os.path.exists(data_file)):
        with open(data_file, "w+"): pass

def save_ui(name : str, IP : str, path : str, spf : str, fps : str, del_img : str):
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
        f.write(name + "\n")
        f.write(IP + "\n")
        f.write(path + "\n")
        f.write(spf + "\n")
        f.write(fps + "\n")
        f.write(del_img + "\n")
        f.write("#######\n")

def load_time_lapse_configs() -> list[str]:
    """Loads all saved configs

    Returns:
        A list which all configs.
    """

    configs = []

    data_file = os.path.join(tempfile.gettempdir(), about.name, about.data_file_name)
    print("loading configs from:", data_file)
    
    file_content = []

    #read the file into an array
    with open(data_file, "r") as f:
        file_content = f.readlines()        

    #find the lines in the array which begin a config (#######)
    config_begun = False
    for line in file_content:
        if(line == "#######\n" and not config_begun):
            config_begun = True
            configs.append([])
            continue
        elif(line == "#######\n" and config_begun):
            config_begun = False
            continue
        
        configs[len(configs) - 1].append(line.replace("\n", ""))
        
    return configs 
