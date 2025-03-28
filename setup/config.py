"""
Este archivo contiene las configuraciones generales del proyecto.
"""



"""
Configuraciones Stiff

fixed_range: bool
    Si se desea que el rango de los ejes sea fijo o no.
x_range: int
    Rango en cada eje X.
chem_data_path: str
    Ruta del archivo de datos químicos.
"""
chem_data_path = "../input/Analisis_AFQ.xlsx"
fixed_range = True
x_range = 25
sample_name = 'Estacion'

#Plot style
facecolor = '#fff419'  # HEX-> '#FF0000'
edgecolor = 'black'
alpha = 1 #Transparencia 0-1
linewidths = 5



"""
Configuraciones Shape Stiff
"""

#Define la estructura del archivo (Geojson).      
schema_stiff = {
    "geometry":"Point",
    "properties": [
        ("Estacion","str"),
        ("HCO3","float"),
        ("CO3", "float"),
        ("SO4","float"),
        ("Cl","float"),
        ("Na","float"),
        ("K","float"),
        ("Ca","float"),
        ("Mg","float"),
        ("Stiff_path","str"),
        ("Stiff_pol_path","str")
        ]
}


#EPSG:4326 WGS84.
#EPSG:3116 MAGNA.
#EPSG:9377 NACIONAL.                                                                  #EPSG:9377 NACIONAL.

shape_config = {
    "shapefile_path": "../results/Shapefiles/test.shp",
    "crs":"EPSG:3116",
    "geometry": "Point",
    "east_name": "Este",
    "north_name": "Norte"
}


"""
Configuraciones csv salida con nuevos datos
- Balance ionico
- Hidrofacies
- Mili equivalentes
"""
chem_data_output_path='../results/Txt/Analisis_AFQ_chem.csv'