import os
import subprocess

def install_requirements(requirements_path):
    if os.path.exists(requirements_path):
        subprocess.check_call(['pip', 'install', '-r', requirements_path])
        print(f"Installed packages from {requirements_path}.")
    else:
        print(f"No {requirements_path} found.")



def create_folders(folders):
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Folder '{folder}' created.")
        else:
            print(f"Folder '{folder}' already exists.")



folders = [
    '../results/Png', 
    '../results/Svg',
    '../results/Txt', 
    '../results/Shapefiles',
    '../input'
    ]

requirements_path = './setup/requirements.txt'

install_requirements(requirements_path)
create_folders(folders)
