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


iones = {
'HCO3': 61, 'CO3' : 30, 'Cl' : 35, 'SO4': 48,
'Na' : 23, 'Ca' : 20, 'Mg' : 12, 'K'  : 39
}



if 'x_range' not in globals() or not isinstance(x_range, (int, float)) or x_range <= 0:
    raise ValueError("x_range config must be a positive number")

total_x_range = x_range * 2



datosQuimica = pd.read_excel("Analisis_AFQ.xlsx")

print(datosQuimica.info())

print(datosQuimica.shape)



datosQuimica['Estacion'] = datosQuimica['Estacion'].str.replace("/","_")
datosQuimica['Estacion'] = datosQuimica['Estacion'].str.replace("–","-")
datosQuimica['Estacion'] = datosQuimica['Estacion'].str.replace(" |%/s","")
datosQuimica = datosQuimica.set_index(['Estacion'])


for ion in iones.keys():
    datosQuimica[str(ion)+'_meq'] = datosQuimica[ion]/iones[ion]

#Guarda archivo para QC
datosQuimica.to_csv('./Txt/Analisis_AFQ.csv')

for index, row in datosQuimica.iterrows():
    Na_K, Ca, Mg = row['Na_meq']+row['K_meq'], row['Ca_meq'], row['Mg_meq'] 
    Cl, HCO3_CO3, SO4 = row['Cl_meq'], row['HCO3_meq']+row['CO3_meq'], row['SO4_meq']

    #apply some factor for the axis
    if not fixed_range:
        total_x_range = max([Na_K, Ca, Mg, Cl, HCO3_CO3, SO4])*2
    #x_range = 494 #max([Na_K, Ca, Mg, Cl, HCO3_CO3, SO4])*2 # Escala en el eje X  50 #
    #set of points of the Stiff diagram
    a = np.array([[0.5 + Cl/total_x_range,1],[0.5 + HCO3_CO3/total_x_range,.5],[0.5 + SO4/total_x_range,0],
                  [0.5 - Mg/total_x_range,0],[0.5 - Ca/total_x_range,.5],[0.5 - Na_K/total_x_range,1]])
    

    figura = diagramaStiff(a, total_x_range, index)
    figura.savefig('./Svg/'+str(index)+'.svg')
    figura.savefig('./Png/'+str(index)+'.png',dpi=100)
    row['stiff_path'] = './Svg/'+str(index)+'.svg'
    #figura.savefig('./Pdf/'+str(index)+'.pdf')
    
####### En esta parte se genera el archivo de puntos con coordenadas ########
####### y el archivo de estilo para los puntos, después se cargan en QGIS ###

#observation point spatial file
datosQuimicaGeo = datosQuimica.loc[:,'Este':'Norte']
datosQuimicaGeo.to_csv('./Txt/Analisis_AFQ_FINAL.csv')

#path to the Svg folder
imagePath = os.path.join(os.path.dirname(os.getcwd()),'Svg')
imagePath = imagePath.replace('\\','/')
imagePath

#'/Users/TIP/Documents/ValleMedioMagdalena/2021/Python/Svg'

#style file generation
archivoestilos = open('./Txt/estilosAnalisis_AFQ_FINAL','w')
archivoestilos.write(encabezado)

for index, row in datosQuimica.iterrows():
    item = re.sub('%%path%%',imagePath,item)
    estiloitem = re.sub('%%index%%',index,item)
    archivoestilos.write(estiloitem)
archivoestilos.write(final)

archivoestilos.close()
