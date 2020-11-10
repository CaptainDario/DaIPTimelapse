#standard
import os, sys
from PySide2.QtCore import QFile, QTextStream
#PySide2
from PySide2.QtWidgets import QApplication, QMainWindow
#custom
import IO
from main_ui import main_ui 
import about
import breeze_resources




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
    window.setWindowTitle(about.name + " - v" + about.version)
    
    window.show()

    ui = main_ui(window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()