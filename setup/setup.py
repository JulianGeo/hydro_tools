import os
import subprocess

def install_requirements():
    requirements_file = 'requirements.txt'
    if os.path.exists(requirements_file):
        subprocess.check_call(['pip', 'install', '-r', requirements_file])
        print(f"Installed packages from {requirements_file}.")
    else:
        print(f"No {requirements_file} found.")

install_requirements()

folders = ['Png', 'Svg', 'Txt', 'Shapefiles']

def create_folders(folders):
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Folder '{folder}' created.")
        else:
            print(f"Folder '{folder}' already exists.")

create_folders()
