
import datetime, time
import requests 
import os



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


    def __init__(self, capture_timeframe : int, url : str, path : str):

        self.capture_timeframe = capture_timeframe
        self.url = url
        self.path = path


    def download_image(self):
        """
        Downloads an image from the given self.url and saves it as self.name + self.pictures_taken to self.path.
        """

        _name =  "test" + "_" + str(self.pictures_taken) + ".jpg"

        img = requests.get(self.url, stream=True)
    