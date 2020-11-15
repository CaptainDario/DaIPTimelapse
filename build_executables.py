#######################################################
#
# This script assumes that a virtual environment with
# all necessary packages AND pyinstaller is in a 
# folder .venv\Scripts\pyinstaller.exe
#
#######################################################
import sys
sys.path.insert(0, "./src")
import about

import os
import shutil
import subprocess



def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print (proc_stdout)


if __name__ == "__main__":
    
    build_command_file = ""
    build_command_folder = ""

    name_folder = ""
    name_file   = ""

    activate_venv_cmd = ""

    #build for WINDOWS
    if(os.name == "nt"):
        activate_venv_cmd = ".venv\\Scripts\\activate.bat"

        data =  "--add-data .\\img;img "
        data += "--add-data .\\ui;ui "
        data += "--add-data .\\styling;styling "
        data += "--add-data .\\src;src "

        #add the whole PySide2 folder (huge size but pyinstaller does not find the correct libs)
        data += "--add-data .\\.venv\\Lib\\site-packages\\PySide2;PySide2"

        path = "--distpath=.\\build\\windows"

        icon = "--icon .\\img\\icon.ico"

        name_folder = str(about.full_id) + "_folder"
        name_file   = str(about.full_id) + "_file"

        build_command_file = " ".join(["pyinstaller", data, path, "--name=" + name_file, "--clean", "--onefile", icon, "--noconfirm", ".\src\main.py"])
        build_command_folder = " ".join(["pyinstaller", data, path, "--name=" + name_folder, "--hidden-import PySide2", "--clean", icon, "--noconfirm", ".\src\main.py"])
    else:
        print("OS on which you are trying to build is not configured.")
        print("Please add a build configuration and submit a pull request: " + about.pull_url)
    
    #print(build_command_file)
    #print(build_command_folder)

    # --- build onefile-exe
    subprocess.call(activate_venv_cmd + " && " + build_command_file)
    #remove spec
    os.remove(name_file + ".spec")
    #remove temp folder
    shutil.rmtree(os.path.join("build", name_file))

    # --- build folder-exe
    subprocess.call(activate_venv_cmd + " &&" + build_command_folder)
    #remove spec
    os.remove(name_folder + ".spec")
    #remove temp folder
    shutil.rmtree(os.path.join("build", name_folder))


