#default
import shutil
import os
import shutil
import cv2
#PySide2
from PySide2 import *
from PySide2.QtCore import QTimer, Qt
from PySide2.QtGui import QIcon
#custom
import IO
import network
import main_ui 



class timelapse(object):
    '''
    Saves all values of a timelapse.
    Also manages the ui for this specific timelapse.

    Attributes:
        capture_timeframe     (int) : the time until the next frame will be captured.
        url                   (str) : the url of the camera stream where the still should be extracted from.
        ipstream (cv2.VideoCapture) : the open video stream from which images will be grabbed.
        path                  (str) : the path were the image should be saved at.
        name                  (str) : a user defined name for the current time lapse.
        fps                   (int) : The framerate of the video render.
        del_img              (bool) : If the images (and folder) should be delted after the video was rendered. 
        pictures_taken        (int) : how many images were already taken.
        timer_take_image   (QTimer) : timer to get an image every x-seconds.
        timer_progressbar  (QTimer) : timer to increase the progressbar every second.
        window_timelapse  (QWindow) : the ui window for the current time lapse.
    '''


    def __init__(self, url : str, path : str, name : str, capture_timeframe : int, fps : int, del_img : bool):
        #instance members
        self.url      = url
        self.ipstream = cv2.VideoCapture(self.url)
        self.path     = path
        self.name     = name
        self.fps      = fps
        self.del_img  = del_img
        self.capture_timeframe = capture_timeframe 
        self.pictures_taken    = 0
        self.timer_take_image  = QTimer()
        self.timer_progressbar = QTimer()
        self.window_timelapse  = IO.load_ui_file(IO.resource_path(os.path.join("ui", "timelapse.ui"))) 
        
        #load icon
        self.window_timelapse.setWindowIcon(QIcon("img/icon.ico"))

        #connect ui and functions
        self.connect_ui()

        #disable the close/maximize button
        self.window_timelapse.setWindowFlags(Qt.Window  | Qt.WindowTitleHint)
        #open ui window
        self.window_timelapse.setWindowTitle(self.name)
        self.window_timelapse.show()
        #set the values to the ones the user has entered
        self.window_timelapse.label_ip.setText(str(self.url))
        self.window_timelapse.label_timelapsePath.setText(str(self.path))
        self.window_timelapse.label_timelapseName.setText(str(self.name))
        self.window_timelapse.label_spf.setText(str(self.capture_timeframe))

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
        Connect the ui of the timelapse-ui with their functions.
        '''
        
        self.window_timelapse.pushButton_finishTimelapse.clicked.connect(self.render_time_lapse)

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

        self.timer_current_value += 1
        self.window_timelapse.progressBar_timeTillNextImage.setValue(self.timer_current_value)
        tmp = self.capture_timeframe - self.timer_current_value
        self.window_timelapse.progressBar_timeTillNextImage.setFormat("Next image in " + str(tmp) + "s")

    def take_image(self):
        """
        Downloads the current image from the given URL.
        Displays it in the "label_lastImageTaken"-label and saves it to the given path.
        """

        #download image from the given url 
        valid = network.check_camera_ip_ui(self.url, self.window_timelapse.label_lastImageTaken)
        ret, frame = self.ipstream.read()
        
        if(ret):
            #process and save image
            rgbImage = frame#cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite(os.path.join(self.path, self.name, "images", self.name + "_" + format(self.pictures_taken, '017d') + ".jpg"), rgbImage)
            self.pictures_taken += 1
        
        #reset the timer until the next image will be taken
        self.timer_current_value = 0 
        self.window_timelapse.progressBar_timeTillNextImage.setValue(self.timer_current_value)
        self.window_timelapse.progressBar_timeTillNextImage.setFormat("Next image in " + str(self.capture_timeframe) + "s")

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
        video = cv2.VideoWriter(os.path.join(self.path, self.name, self.name + ".mp4"), fourcc, self.fps, (w, h))

        #change the color space and render the video
        for img in images:
            image = cv2.imread(img)
            video.write(image)

        video.release()

        #delete the folder with the images if user checked the box
        if(self.del_img):
            shutil.rmtree(img_dir)

        #close the window
        self.window_timelapse.close()
        #delete this timelapse
        self.del_timelapse()

    def del_timelapse(self):
        """Delete this timelapse object so that the garbage collector can remove it.
        """
        
        main_ui.main_ui.current_timelapses.remove(self)
        self = None


