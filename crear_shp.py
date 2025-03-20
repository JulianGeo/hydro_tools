# -*- coding: utf-8 -*-
import fiona
import pandas as pd


"""
Crea un archivo shapefile a partir de un dataframe de pandas.

Parameters
----------
dataframe : pandas.DataFrame
    Dataframe con los datos a guardar en el shapefile.
geojson_schema : dict
    Esquema del archivo geojson.
shape_config : dict
    Configuraciones del shapefile.
shape_properties : list of dict
    Lista de diccionarios con las propiedades de cada poligono.
"""
def create_shape(
        dataframe, 
        geojson_schema, 
        shape_config,
        shape_properties
    ):

    #Crea el archivo shp.
    shapefile = fiona.open(
        shape_config.get("shapefile_path"),
        mode="w",
        driver="ESRI Shapefile",
        schema=geojson_schema,
        crs=shape_config.get("crs")
    )

    #Ingresa los datos para cada poligono a guardar en el shapefile.

    i=0
    for index, row in dataframe.iterrows():
        #print(shape_properties.get('HCO3'), '###########')
        rowDict = {
            "geometry":{
                "type":shape_config.get("geometry"),
                "coordinates":[
                    row[shape_config.get("east_name")],
                    row[shape_config.get("north_name")]]
                },
                "properties": shape_properties[i]
        }
        #print(rowDict)
        shapefile.write(rowDict)
        i+=1

    shapefile.close()
    #print(rowDict)

