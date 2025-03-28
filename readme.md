# Project README

## Overview

This directory contains Python scripts for the `Hydro tools` project. These scripts are designed to perform various tasks and automate processes related to the project.

## Requirements

- Python 3.x
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository:
    ```sh
    git clone [https://github.com/JulianGeo/hydro_tools.git](https://github.com/JulianGeo/hydro_tools.git)
    ```
2. Navigate to the project directory:
    ```sh
    cd hydro_tools/scripts
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To run a specific script, use the following command:
```sh
python script_name.py
```
Replace `script_name.py` with the name of the script you want to execute.


## QGIS integration
Once the images are generated, the results folder should be copied to the QGIS project root directory. The SVG or PNG files can then be linked to the shapefile representation using their relative paths.

## Backlog
- Revisar integración con Arcgis
- Ojear el shape de poligono
- Implementar Autoescala
- Crear flujo para calcular y generar excel con nueva data química (miliquivalentes, hidrofacies, balance ionico)



