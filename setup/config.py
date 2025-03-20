"""
Este archivo contiene las configuraciones generales del proyecto.
"""



"""
Configuraciones Stiff

fixed_range: bool
    Si se desea que el rango de los ejes sea fijo o no.
x_range: int
    Rango en cada eje X.
"""
fixed_range = True
x_range = 10






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
        ("Stiff_path","str")
        ]
}


#EPSG:4326 WGS84.
#EPSG:3116 MAGNA.
#EPSG:9377 NACIONAL.                                                                  #EPSG:9377 NACIONAL.

shape_config = {
    "shapefile_path": "Shapefiles/test.shp",
    "crs":"EPSG:3116",
    "geometry": "Point",
    "east_name": "Este",
    "north_name": "Norte"
}