#default
import requests 
import shutil
import os
import threading
#PySide2
from PySide2.QtWidgets import QLabel, QMessageBox
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QByteArray, QTimer
#custom
import IO
import network



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
    timer_take_image = None
    #timer to increase the progressbar every second
    timer_progressbar = None


    def __init__(self, url : str, path : str, name : str, capture_timeframe : int):

        self.url  = url
        self.path = path
        self.name = name
        self.capture_timeframe      = capture_timeframe
        
        #open ui window
        self.window_timelapse = IO.load_ui_file(os.path.join("ui", "timelapse.ui")) 
        self.window_timelapse.setWindowTitle(self.name)
        self.window_timelapse.show()
        #set the values to the ones the user has entered
        self.window_timelapse.label_ip.setText("IP-address: " + str(self.url))
        self.window_timelapse.label_timelapsePath.setText("timelapse path: " + str(self.path))
        self.window_timelapse.label_timelapseName.setText("name: " + str(self.name))
        self.window_timelapse.label_spf.setText("spf: " + str(self.capture_timeframe))

        #create the folder where the images of the timelapse wil be saved
        self.create_timelapse_folder()

        #setup the progressbar which indicates when a new image will be taken
        self.timer_current_value = 0
        self.window_timelapse.progressBar_timeTillNextImage.setRange(0, self.capture_timeframe * 1000)
        self.timer_progressbar = QTimer()
        self.timer_progressbar.setInterval(1000)
        self.timer_progressbar.timeout.connect(self.increase_progressBar)
        self.timer_progressbar.start()

        #start taking images
        self.timer_take_image = QTimer()
        self.timer_take_image.setInterval(self.capture_timeframe * 1000)
        self.timer_take_image.timeout.connect(self.take_image)
        self.timer_take_image.start()

    def connect_ui(self):
        '''
        Connect the buttons of the timelapse-ui with their functions.
        '''
        #FINISH BUTTON
        #REMOVE TIMELAPSE FROM TIMELAPSE ARRAY WHEN CLOSED
        pass

    def create_timelapse_folder(self):
        """
        Creates the folder in which the video and images of the timelapse should be stored.
        """
        
        os.mkdir(os.path.join(self.path, self.name))
        os.mkdir(os.path.join(self.path, self.name, "images"))

    def increase_progressBar(self):
        '''
        '''

        self.timer_current_value += 1000
        self.window_timelapse.progressBar_timeTillNextImage.setValue(self.timer_current_value)


    def take_image(self):
        """
        Downloads the current image from the given URL.
        Displays it in the "label_lastImageTaken"-label and saves it to the given path.

        TODO:
            Save the image to file
        """

        #download image from the given url 
        valid = network.check_camera_ip(self.url, self.window_timelapse.label_lastImageTaken)
        if(not valid):
            QMessageBox.critical(None, "Error", ("An unexpected error appeared during image downloading/conversion! \n" + \
                                        "Please check that the IP-camera is returning a valid image and the URL is set correctly."))


        #reset the timer until the next image will be taken
        self.window_timelapse.progressBar_timeTillNextImage.reset()
        self.timer_current_value = 0


    