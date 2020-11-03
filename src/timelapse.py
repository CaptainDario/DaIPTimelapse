#default
import requests 
import shutil
import os
import cv2
#PySide2
from PySide2.QtWidgets import QLabel, QMessageBox
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QByteArray, QTimer
#custom
import IO
import network



class timelapse(object):
    '''
    Saves all values of a timelapse.
    Also manages the ui for this specific timelapse.

    Attributes:
        capture_timeframe    (int) : the time until the next frame will be captured.
        url                  (str) : the url of the camera stream where the still should be extracted from
        path                 (str) : the path were the image should be saved at
        name                 (str) : a user defined name for the current time lapse
        pictures_taken       (int) : how many images were already taken
        timer_take_image  (QTimer) : timer to get an image every x-seconds
        timer_progressbar (QTimer) : timer to increase the progressbar every second
        window_timelapse (QWindow) : the ui window for the current time lapse
    '''


    def __init__(self, url : str, path : str, name : str, capture_timeframe : int):

        #instance members
        self.url  = url
        self.path = path
        self.name = name
        self.capture_timeframe = capture_timeframe
        self.pictures_taken = 0
        self.timer_take_image = QTimer()
        self.timer_progressbar = QTimer()
        self.window_timelapse = IO.load_ui_file(os.path.join("ui", "timelapse.ui")) 

        #connect ui and functions
        self.connect_ui()

        #open ui window
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
        self.timer_current_value = self.capture_timeframe
        self.window_timelapse.progressBar_timeTillNextImage.setRange(0, self.capture_timeframe)
        #self.window_timelapse.progressBar_timeTillNextImage.setText("Progress until next image")
        self.timer_progressbar.setInterval(1000)
        self.timer_progressbar.timeout.connect(self.increase_progressBar)
        self.timer_progressbar.start()

        #take a first image
        self.take_image()

        #start taking images
        self.timer_take_image.setInterval(self.capture_timeframe * 1000)
        self.timer_take_image.timeout.connect(self.take_image)
        self.timer_take_image.start()

    def connect_ui(self):
        '''
        Connect the buttons of the timelapse-ui with their functions.
        '''
        self.window_timelapse.pushButton_finishTimelapse.clicked.connect(self.render_time_lapse)
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
        Show the time until the next image will be taken in the progressbar.
        '''

        self.timer_current_value -= 1
        self.window_timelapse.progressBar_timeTillNextImage.setValue(self.timer_current_value)
        self.window_timelapse.progressBar_timeTillNextImage.setFormat("Next image in %v s")


    def take_image(self):
        """
        Downloads the current image from the given URL.
        Displays it in the "label_lastImageTaken"-label and saves it to the given path.
        """

        #download image from the given url 
        valid = network.check_camera_ip(self.url, self.window_timelapse.label_lastImageTaken)
        if(not valid):
            QMessageBox.critical(None, "Error", ("An unexpected error appeared during image downloading/conversion! \n" + \
                                        "Please check that the IP-camera is returning a valid image and the URL is set correctly."))
        #save image to the time lapse path
        if(valid):
            #connect to stream
            cap = cv2.VideoCapture(self.url)

            ret, frame = cap.read()
            if(ret):
                #process and save image
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imwrite(os.path.join(self.path, self.name, "images", self.name + "_" + format(self.pictures_taken, '017d') + ".jpg"), rgbImage)
                self.pictures_taken += 1
        
        #reset the timer until the next image will be taken
        self.timer_current_value = self.capture_timeframe
        self.window_timelapse.progressBar_timeTillNextImage.setValue(self.timer_current_value)
        self.window_timelapse.progressBar_timeTillNextImage.setFormat("Next image in %v s")

    def render_time_lapse(self):
        '''
        Render a time lapse from all images taken from the time lapse.
        '''

        img_dir = os.path.join(self.path, self.name, "images")

        #read all frames (full path!) from the folder
        images = [os.path.join(img_dir, img) for img in os.listdir(img_dir) if img.endswith(".jpg")]

        #get the dim of the video
        h, w, ch = cv2.imread(images[0]).shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        video = cv2.VideoWriter(os.path.join(self.path, self.name, self.name + ".mp4"), fourcc, 1, (w, h))

        for img in images:
            video.write(cv2.imread(img))

        video.release()


