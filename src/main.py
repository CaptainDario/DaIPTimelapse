#standard
import os, sys
#PySide2
from PySide2.QtWidgets import QApplication, QMainWindow
#custom
import IO
import ui_elements
import about



def main():
    app = QApplication(sys.argv)

    #load the ui from file
    window = IO.load_ui_file(os.path.join("ui", "main.ui")) 
    window.setWindowTitle(about.name + " - " + about.version)
    window.show()

    main_ui = ui_elements.main_ui(window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()