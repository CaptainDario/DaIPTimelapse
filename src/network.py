import cv2
import requests
import re

from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtCore import Qt

import about



def check_camera_ip(ipaddr : str, label : QLabel):
    '''
    Checks if the given String is a valid ip-address which leads to a camera-/image-stream.
    If that is the case the downloaded image will be applied to the given label.
    Otherwise an error message will be written.

    Args:
        ipaddr : 
        label

    Returns:
        True, if an image was successfully downloaded and applied to the label.
        False otherwise.
    '''

    valid = False

    lw = label.width()
    #connect to stream
    cap = cv2.VideoCapture(ipaddr)

    ret, frame = cap.read()
    if(ret):
        #process image
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        #convert to fit into label
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(lw, 480, Qt.KeepAspectRatio)
        label.setPixmap(QPixmap(p))

        valid = True

    return valid

def check_for_update():
    """Checks if there is a newer version available at github then the one currently running.

    Returns:
        True if there is a new version and False otherwise.
    """

    new_version_av = False

    print("You are running DaIPTimelapse v" + about.version)

    newest_ver_req = requests.get(about.latest_release_api)
    if(newest_ver_req.ok):
        #get the version from github release
        newest_ver = newest_ver_req.json()["tag_name"]
        new_version = re.search("\d+\.\d+", newest_ver)[0]

        #compare
        old, new = float(about.version), float(new_version)

        if(old < new):
            print("There is an update available!")
            new_version_av = True
        else:
            print("This is the latest version available.")

    else:
        print("Could not connect to github server.")

    return new_version_av
