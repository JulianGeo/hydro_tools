# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import re, os

from funciones import *
from variables import *
from setup.config import *
from crear_shp import *


iones = {
'HCO3': 61, 'CO3' : 30, 'Cl' : 35, 'SO4': 48,
'Na' : 23, 'Ca' : 20, 'Mg' : 12, 'K'  : 39
}


if 'x_range' not in globals() or not isinstance(x_range, (int, float)) or x_range <= 0:
    raise ValueError("x_range config must be a positive number")

total_x_range = x_range * 2



datosQuimica = pd.read_excel(chem_data_path)

print(datosQuimica.info())

print(datosQuimica.shape)



datosQuimica['Estacion'] = datosQuimica['Estacion'].str.replace("/","_")
datosQuimica['Estacion'] = datosQuimica['Estacion'].str.replace("–","-")
datosQuimica['Estacion'] = datosQuimica['Estacion'].str.replace(" |%/s","")
datosQuimica = datosQuimica.set_index(['Estacion'])


for ion in iones.keys():
    datosQuimica[str(ion)+'_meq'] = datosQuimica[ion]/iones[ion]


for index, row in datosQuimica.iterrows():
    Na_K, Ca, Mg = row['Na_meq']+row['K_meq'], row['Ca_meq'], row['Mg_meq'] 
    Cl, HCO3_CO3, SO4 = row['Cl_meq'], row['HCO3_meq']+row['CO3_meq'], row['SO4_meq']

    #apply some factor for the axis
    if not fixed_range:
        total_x_range = max([Na_K, Ca, Mg, Cl, HCO3_CO3, SO4])*2
    #x_range = 494 #max([Na_K, Ca, Mg, Cl, HCO3_CO3, SO4])*2 # Escala en el eje X  50 #
    #set of points of the Stiff diagram
    a = np.array([
        [0.5 + Cl/total_x_range,1],
        [0.5 + HCO3_CO3/total_x_range,.5],
        [0.5 + SO4/total_x_range,0],
        [0.5 - Mg/total_x_range,0],
        [0.5 - Ca/total_x_range,.5],
        [0.5 - Na_K/total_x_range,1]
        ])
    
    figura = diagramaStiff(a, total_x_range, index)
    figura.savefig('../results/Svg/'+str(index)+'.svg')
    figura.savefig('../results/Png/'+str(index)+'.png',dpi=100)
    datosQuimica.loc[index, 'stiff_path'] = os.path.abspath('../results/Svg/'+str(index)+'.svg')
    #figura.savefig('./Pdf/'+str(index)+'.pdf')

#Guarda archivo para QC
datosQuimica.to_csv('../results/Txt/Analisis_AFQ.csv')

####### En esta parte se genera el archivo de puntos con coordenadas ########
####### y el archivo de estilo para los puntos, después se cargan en QGIS ###

#observation point spatial file
datosQuimicaGeo = datosQuimica.loc[:,'Este':'Norte']
datosQuimicaGeo.to_csv('../results/Txt/Analisis_AFQ_FINAL.csv')

#path to the Svg folder
imagePath = os.path.join('../results/Svg')
imagePath = imagePath.replace('\\','/')

#'/Users/TIP/Documents/ValleMedioMagdalena/2021/Python/Svg'

#style file generation
archivoestilos = open('../results/Txt/estilosAnalisis_AFQ_FINAL','w')
archivoestilos.write(encabezado)

for index, row in datosQuimica.iterrows():
    item = re.sub('%%path%%',imagePath,item)
    estiloitem = re.sub('%%index%%',index,item)
    archivoestilos.write(estiloitem)
archivoestilos.write(final)

archivoestilos.close()


## Shapefile creation
shape_properties = []
for index, row in datosQuimica.iterrows():
    shape_properties.append({
        "Estacion": index,
        "HCO3": row['HCO3'],
        "CO3": row['CO3'],
        "SO4": row['SO4'],
        "Cl": row['Cl'],
        "Na": row['Na'],
        "K": row['K'],
        "Ca": row['Ca'],
        "Mg": row['Mg'],
        "Stiff_path": row['stiff_path']
    })

create_shape(
    datosQuimica, 
    schema_stiff, 
    shape_config, 
    shape_properties
    )
