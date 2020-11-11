#standard
import os, sys
import webbrowser
from PySide2.QtCore import QFile, QTextStream
#PySide2
from PySide2.QtWidgets import QApplication, QMainWindow
#custom
import IO
from main_ui import main_ui 
import about
import breeze_resources
import network




def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    #load the dark style
    file = QFile(IO.resource_path(os.path.join("styling", "dark.qss")))
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    #load the ui from file
    window = IO.load_ui_file(IO.resource_path(os.path.join("ui", "main.ui"))) 
    window.setWindowTitle(about.full_id)
    
    window.show()

    #check for newer version
    if(network.check_for_update()):
        u_window = IO.load_ui_file(IO.resource_path(os.path.join("ui", "update.ui"))) 
        u_window.setWindowTitle("Update available")
        u_window.pushButton_download.clicked.connect(lambda : webbrowser.open(about.latest_release_url))
        u_window.pushButton_close.clicked.connect(lambda : u_window.close())
        u_window.show()
        

    ui = main_ui(window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()