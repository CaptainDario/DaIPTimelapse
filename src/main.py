#standard
import os, sys
from PySide2.QtCore import QFile, QTextStream
#PySide2
from PySide2.QtWidgets import QApplication, QMainWindow
#custom
import IO
import ui_elements
import about
import breeze_resources




def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    #load the dark style
    file = QFile(os.path.join("styling", "dark.qss"))
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    #load the ui from file
    window = IO.load_ui_file(os.path.join("ui", "main.ui")) 
    window.setWindowTitle(about.name + " - " + about.version)
    
    window.show()

    main_ui = ui_elements.main_ui(window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()