#standard
import urllib.request
import datetime, time
import sched
import os, sys
import requests 
#custom
import ui
#PySide2
from PySide2.QtCore import QByteArray
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel
from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtGui import QPixmap, QImage



#the time until the next frame will be captured
capture_timeframe = 0
#the url of the camera stream where the still should be extracted from
url = ""
#the path were the image should be saved at
path = ""


def download_image(_url : str, _path : str = "", _name : str = "", _include_tick_nr : str = ""):
    """
    Downloads an image from the given _url and saves it as _name to _path.

    Args:
        _url  : the url from which the image will be downloaded
        _path : [optional] the path where the image should be saved (WITHOUT filename)
        _name : [optional] the name the image should be saved as (WITHOUT fileextension)
                if left empty the current date and time will be used as the name
    """

    #set the current datetime if no name is passed
    if(_name == ""):
        _name = str(datetime.datetime.now()).replace(" ", "").replace(":", "").replace("-", "").replace(".", "")

    #add the nr of the tick to the name if arg is set
    if(_include_tick_nr != ""):
        _name =  _name + "_" + str(_include_tick_nr) + ".jpg"

    urllib.request.urlretrieve(_url, os.path.join(_path, _name))


def main():

    #capture loop
    starttime = time.time()
    #count the nr of images which were already taken
    ticks = 0

    while True:
        ticks += 1
        print("tick:", ticks)

        download_image(url, _path=path, _name="PSU_cover_shroud", _include_tick_nr=str(ticks))

        #wait for the next time a image should be taken
        time.sleep(capture_timeframe - ((time.time() - starttime) % capture_timeframe))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    #load the ui from file
    window = ui.load_ui_file(os.path.join("ui", "main.ui")) 
    window.show()

    #test
    label_video_stream = window.findChild(QLabel, "label_video_stream")

    label_pixmap = None
    url = "http://192.168.178.51/webcam/?action=stream"
    #url = "https://cdn.pixabay.com/photo/2017/08/30/01/05/milky-way-2695569__340.jpg"
    if(url == ""):
        label_pixmap = QPixmap(os.path.join("img", "placeholder.png"))
    else:
        img = requests.get(url, stream=True)
        img.raw.decode_content = True
        #qimg = QImage.loadFromData(img.content)
        label_pixmap = QPixmap()
        label_pixmap.loadFromData(QByteArray(img.raw.data))
    label_video_stream.setPixmap(label_pixmap)
    label_video_stream.setMask(label_pixmap.mask())

    sys.exit(app.exec_())
