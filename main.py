#standard
import sched
import os, sys
import requests
#custom
import ui
#PySide2
from PySide2.QtWidgets import QApplication, QMainWindow


def main():
    app = QApplication(sys.argv)

    #load the ui from file
    window = ui.load_ui_file(os.path.join("ui", "main.ui")) 
    window.show()


    sys.exit(app.exec_())


if __name__ == "__main__":
    main()