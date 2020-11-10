import os
import subprocess



if __name__ == "__main__":
    
    build_command = ""

    #build for window
    if(os.name == "nt"):
        data =  "--add-data .\\img;img "
        data += "--add-data .\\ui;ui "
        data += "--add-data .\\styling;styling "
        data += "--add-data .\\.venv\\Lib\\site-packages\\PySide2;PySide2"

        path = "--distpath=.\\build\\windows"

        icon = ""

        name = "--name=DaIPTimelapse"

        build_command = " ".join(["pyinstaller", data, path, hidden_imports, name, "--clean", "--noconfirm", ".\src\main.py"])

    
    print(build_command)