import requests

from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QByteArray


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

    try:
        w = label.width()
        #download image
        img = requests.get(ipaddr, stream=True)

        if(img.status_code == 200):
            #decode and transform download
            img.raw.decode_content = True
            label_pixmap = QPixmap()
            label_pixmap.loadFromData(QByteArray(img.raw.data))
            if(label_pixmap is not None):
                #apply the image to the label
                label.setPixmap(label_pixmap.scaledToWidth(w))
            else:
                print("An unexpected error appeared during image downloading/conversion!")
                print("Please check that the IP-camera is returning a valid image and the URL is set correctly.")
        valid = True
    except:
        label.setText("An unexpected error appeared during image downloading/conversion!")
        valid = False

    return valid