# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import re, os
from re import match

from funciones import *
from variables import *
from setup.config import *
from crear_shp import *



if 'fixed_range' not in globals() or not isinstance(fixed_range, bool):
    raise ValueError("fixed_range config must be a boolean")

datosQuimica = pd.read_excel(chem_data_path)

print(datosQuimica.info())
print(datosQuimica.shape)


datosQuimica= clean_sample_names(datosQuimica, sample_name)
datosQuimica = datosQuimica.set_index([sample_name])


datosQuimicaMeq = calculo_milieq(datosQuimica)

names = list(datosQuimicaMeq)
meq = [] 
for i, name in enumerate(names):
    if match(".*_meq",name):
        meq.append(i)

if fixed_range:
    total_x_range = round((datosQuimicaMeq.iloc[:,meq[0]:meq[-1]]).to_numpy().max(),2)*2


for index, row in datosQuimicaMeq.iterrows():
    Na_K, Ca, Mg = row['Na_meq']+row['K_meq'], row['Ca_meq'], row['Mg_meq'] 
    Cl, HCO3_CO3, SO4 = row['Cl_meq'], row['HCO3_meq']+row['CO3_meq'], row['SO4_meq']

    #apply some factor for the axis
    if not fixed_range:
        total_x_range = max([Na_K, Ca, Mg, Cl, HCO3_CO3, SO4])*2

    #set of points of the Stiff diagram
    #refactor this to a function
    ion_data = np.array([
        [0.5 + min(Cl/total_x_range, 0.5), 1],
        [0.5 + min(HCO3_CO3/total_x_range, 0.5), .5],
        [0.5 + min(SO4/total_x_range, 0.5), 0],
        [0.5 - min(Mg/total_x_range, 0.5), 0],
        [0.5 - min(Ca/total_x_range, 0.5), .5],
        [0.5 - min(Na_K/total_x_range, 0.5), 1]
        ])
    
    color = get_stiff_color(fixed_color, data_type, row)
    figura_labels = diagramaStiff(ion_data, total_x_range, index, True, color)
    figura_labels.savefig('../results/Svg/'+str(index)+'.svg')
    figura_labels.savefig('../results/Png/'+str(index)+'.png',dpi=100)
    datosQuimicaMeq.loc[index, 'stiff_path'] = '/results/Svg/'+str(index)+'.svg'
    #figura.savefig('./Pdf/'+str(index)+'.pdf')

    figura_no_labels = diagramaStiff(ion_data, total_x_range, index, False, color)
    figura_no_labels.savefig('../results/Svg/'+str(index)+'_poligono.svg')
    figura_no_labels.savefig('../results/Png/'+str(index)+'_poligono.png',dpi=100)
    datosQuimicaMeq.loc[index, 'Stiff_pol_path'] = '/results/Svg/'+str(index)+'_poligono.svg'

#Guarda archivo para QC
datosQuimicaMeq.to_csv('../results/Txt/Analisis_AFQ.csv')

####### En esta parte se genera el archivo de puntos con coordenadas ########
####### y el archivo de estilo para los puntos, después se cargan en QGIS ###

#observation point spatial file
datosQuimicaGeo = datosQuimicaMeq.loc[:,'Este':'Norte']
datosQuimicaGeo.to_csv('../results/Txt/Analisis_AFQ_FINAL.csv')

#path to the Svg folder
imagePath = os.path.join('../results/Svg')
imagePath = imagePath.replace('\\','/')

#'/Users/TIP/Documents/ValleMedioMagdalena/2021/Python/Svg'

#style file generation
archivoestilos = open('../results/Txt/estilosAnalisis_AFQ_FINAL.sld','w')
archivoestilos.write(encabezado)

for index, row in datosQuimicaMeq.iterrows():
    item = re.sub('%%path%%',imagePath,item)
    estiloitem = re.sub('%%index%%',index,item)
    archivoestilos.write(estiloitem)
archivoestilos.write(final)

archivoestilos.close()


## Shapefile creation
shape_properties = []
for index, row in datosQuimicaMeq.iterrows():
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
        "Stiff_path": row['stiff_path'],
        "Stiff_pol_path": row['Stiff_pol_path']
    })

create_shape(
    datosQuimicaMeq, 
    schema_stiff, 
    shape_config, 
    shape_properties
    )
