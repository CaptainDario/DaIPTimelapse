#default
import requests 
import shutil
import os
import threading
#PySide2
from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QByteArray, QTimer



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
    #timer to get an image every x-seconds
    timer = None

    label_video_stream     = None
    label_last_image_taken = None


    def __init__(self, url : str, path : str, name : str, capture_timeframe : int,
                label_video_stream : QLabel, label_last_image_taken : QLabel):

        self.url  = url
        self.path = path
        self.name = name
        self.capture_timeframe      = capture_timeframe
        self.label_video_stream     = label_video_stream
        self.label_last_image_taken = label_last_image_taken

        self.create_timelapse_folder()

        #start taking images
        self.timer = QTimer()
        self.timer.setInterval(self.capture_timeframe * 1000)
        self.timer.timeout.connect(self.take_image)
        self.timer.start()

    def create_timelapse_folder(self):
        """
        Creates the folder in which the video and images of the timelapse should be stored.
        """

        os.mkdir(os.path.join(self.path, self.name))
        os.mkdir(os.path.join(self.path, self.name, "images"))

    def take_image(self):
        """
        Downloads the current image from the given URL.
        Displays it in the "last_image_taken"-label and saves it to the given path.
        """
        #download image from the given url 
        img = requests.get(self.url, stream=True)
        if(img.status_code == 200):
            img.raw.decode_content = True
            label_pixmap = QPixmap()
            label_pixmap.loadFromData(QByteArray(img.raw.data))
            #resize image and show it in the last frame label
            label_pixmap = label_pixmap.scaledToWidth(self.label_last_image_taken.width())
            self.label_last_image_taken.setPixmap(label_pixmap)

            #save the image
            with open(os.path.join(self.path, self.name, "images", str(self.pictures_taken) + ".jpg"), "wb") as f:
                f.write(img.raw.data)

            self.pictures_taken += 1


    