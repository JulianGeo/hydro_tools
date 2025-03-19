# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 14:47:21 2023

@author: Chiky
"""

import fiona
import pandas as pd

polyData = pd.read_csv("./Fiona/Llanito-4_Yarigui-25_Casabe-1176_Someras_poligonos.csv", sep=",", header=0)
muestras = pd.read_csv("./Fiona/Llanito-4_Yarigui-25_Casabe-1176_Someras_muestras.csv", sep=",", header=0) #Tabla con solo las muestras.

#columnas = polyData.columns
#print(columnas)

#Genera lista de tuplas con las coordenadas de todos los puntos.
lista = []
for index, row in polyData.iterrows():
    lista.append((row.Este,row.Norte))
#print(lista)
#print(len(lista))
#print()

#Genera listas con los atributos a incluir en el shapefile.
names,hco3,co3,so4,cl,na,k,ca,mg,hidrofacies,hidro_res = [],[],[],[],[],[],[],[],[],[],[]
prof = []
pto = []

for index, row in muestras.iterrows():
    names.append(row.Estacion)
    #locacion.append(row.Locacion)
    hco3.append(row.HCO3)
    co3.append(row.CO3)
    so4.append(row.SO4)
    cl.append(row.Cl)
    na.append(row.Na)
    k.append(row.K)
    ca.append(row.Ca)
    mg.append(row.Mg)
    prof.append(row.Profundidad)
    #pto.append(row.Punto)
    hidrofacies.append(row.Hidrofacies)
    hidro_res.append(row.Hidrofacies_res)

#Genera lista de listas de tuplas que corresponde a cada grupo de puntos que formaran los
#poligonos que representan los diagramas de STIFF.

lista_seis = []
lista_final = []
for i in range(len(lista)):
    lista_seis.append(lista[i])
    if len(lista_seis) == 6:
        lista_final.append(lista_seis)
        lista_seis = []
#print(lista_final)
#print(len(lista_final))

#Define la estructura del archivo (Geojson).      
schema = {
    "geometry":"Polygon",
    "properties": [("Estacion","str"),("HCO3","float"),("CO3", "float"),
                   ("SO4","float"),("Cl","float"),("Na","float"),("K","float"),("Ca","float"),
                   ("Mg","float"),("Profundidad","str"),("Hidrofacies","str"),("HidroFa_res","str")]
    }

#Crea el archivo shp.
polyShp = fiona.open("./Fiona/Shapefiles/Llanito-4_Yarigui-25_Casabe-1176_Someras.shp",mode="w", 
                     driver="ESRI Shapefile",schema=schema, crs="EPSG:3116")#EPSG:4326 WGS84.
                                                                            #EPSG:3116 MAGNA.
                                                                            #EPSG:9377 NACIONAL.

#Ingresa los datos para cada poligono a guardar en el shapefile.
for i in range(len(names)):
    rowDict = {"geometry":{"type":"Polygon","coordinates":[lista_final[i]]},
               "properties":{"Estacion":names[i],"HCO3":hco3[i],
                             "CO3":co3[i],"SO4":so4[i],"Cl":cl[i],"Na":na[i],"K":k[i],"Ca":ca[i],
                             "Mg":mg[i],"Profundidad":prof[i],"Hidrofacies":hidrofacies[i],"HidroFa_res":hidro_res[i]}}
    #print(rowDict)
    polyShp.write(rowDict)

polyShp.close()
#print(rowDict)