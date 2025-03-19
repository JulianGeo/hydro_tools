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

iones = {
'HCO3': 61, 'CO3' : 30, 'Cl' : 35, 'SO4': 48,
'Na' : 23, 'Ca' : 20, 'Mg' : 12, 'K'  : 39
}

datosQuimica = pd.read_excel("Analisis_AFQ.xlsx")

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
    maxConNorm = 494 #max([Na_K, Ca, Mg, Cl, HCO3_CO3, SO4])*2 # Escala en el eje X  50 #
    #set of points of the Stiff diagram
    a = np.array([[0.5 + Cl/maxConNorm,1],[0.5 + HCO3_CO3/maxConNorm,.5],[0.5 + SO4/maxConNorm,0],
                  [0.5 - Mg/maxConNorm,0],[0.5 - Ca/maxConNorm,.5],[0.5 - Na_K/maxConNorm,1]])
    

    figura = diagramaStiff(a, maxConNorm, index)
    figura.savefig('./Svg/'+str(index)+'.svg')
    figura.savefig('./Png/'+str(index)+'.png',dpi=100)
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
