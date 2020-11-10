import cv2

from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtCore import QByteArray, Qt 


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