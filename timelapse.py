
import datetime, time
import requests 
import os
#PySide2



class timelapse(object):


    #the time until the next frame will be captured
    capture_timeframe = 0
    #the url of the camera stream where the still should be extracted from
    url = ""
    #the path were the image should be saved at
    path = ""
    #a user defined name for the current time lapse
    name = ""
    #how many images were already taken
    pictures_taken = 0


    def __init__(self, url : str, path : str, name : str, capture_timeframe : int):

        self.url = url
        self.path = path
        self.name = name
        self.capture_timeframe = capture_timeframe


    def download_image(self):
        """
        Downloads an image from the given self.url and saves it as self.name + self.pictures_taken to self.path.
        """

        _name =  "test" + "_" + str(self.pictures_taken) + ".jpg"

        img = requests.get(self.url, stream=True)


        #test

        label_pixmap = None
        #url = "http://192.168.178.51/webcam/?action=snapshot"
        #if(url == ""):
        #    label_pixmap = QPixmap(os.path.join("img", "placeholder.png"))
        #else:
        #    img = requests.get(url, stream=True)
        #    img.raw.decode_content = True
        #    #qimg = QImage.loadFromData(img.content)
        #    label_pixmap = QPixmap()
        #    label_pixmap.loadFromData(QByteArray(img.raw.data))
        #label_video_stream.setPixmap(label_pixmap)
        #label_video_stream.setMask(label_pixmap.mask())
    