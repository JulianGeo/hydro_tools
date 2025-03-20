# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 08:34:38 2021

@author: TIP
"""

import pandas as pd
import numpy as np
import os, math
import matplotlib.pyplot as plt
import imageio

from hidrofacies import hidrofacies, print_hidrofacies

img = imageio.imread("./Figures/PiperCompleto.png")

datosQuimica = pd.read_excel('./Xls/Analisis_AFQ.xlsx')
#print(datosQuimica.info())
#columnas = list(datosQuimica.columns)
#print(columnas)
nombres = datosQuimica['Estacion'] #Regresa nombre de las muestras se usa en las funciones.

datosQuimica['Estacion'] = datosQuimica['Estacion'].str.replace("/", "_")
datosQuimica['Estacion'] = datosQuimica['Estacion'].str.replace("â€“", "-")
datosQuimica['Estacion'] = datosQuimica['Estacion'].str.replace("|%/s", "")
datosQuimica = datosQuimica.set_index(['Estacion'])

datosQuimica.head()

iones = {
    'HCO3': 61, 'CO3': 30, 'Cl': 35, 'SO4': 48,
    'Na': 23, 'Ca': 20, 'Mg': 12, 'K': 39
    }

for ion in iones.keys():
    datosQuimica[str(ion)+'_meq'] = datosQuimica[ion]/iones[ion]

datosQuimica.head()

datosQuimica['SO4_norm'] = datosQuimica['SO4_meq'] / (datosQuimica['SO4_meq'] +
                           datosQuimica['HCO3_meq']+datosQuimica['CO3_meq']+datosQuimica['Cl_meq']) * 100
datosQuimica['HCO3_CO3_norm'] = (datosQuimica['HCO3_meq']+datosQuimica['CO3_meq']) / (datosQuimica['SO4_meq'] +
                                datosQuimica['HCO3_meq']+datosQuimica['CO3_meq']+datosQuimica['Cl_meq']) * 100
datosQuimica['Cl_norm'] = datosQuimica['Cl_meq'] / (datosQuimica['SO4_meq'] +
                          datosQuimica['HCO3_meq']+datosQuimica['CO3_meq']+datosQuimica['Cl_meq']) * 100
datosQuimica['Mg_norm'] = datosQuimica['Mg_meq'] / (datosQuimica['Mg_meq'] +
                          datosQuimica['Ca_meq']+datosQuimica['K_meq']+datosQuimica['Na_meq']) * 100
datosQuimica['Na_K_norm'] = (datosQuimica['K_meq']+datosQuimica['Na_meq']) / (datosQuimica['Mg_meq'] +
                             datosQuimica['Ca_meq']+datosQuimica['K_meq']+datosQuimica['Na_meq']) * 100
datosQuimica['Ca_norm'] = datosQuimica['Ca_meq'] / (datosQuimica['Mg_meq'] +
                          datosQuimica['Ca_meq']+datosQuimica['K_meq']+datosQuimica['Na_meq']) * 100

def coordenada(Ca,Mg,Cl,SO4,Label):
    xcation = 40 + 360 - (Ca + Mg / 2) * 3.6
    ycation = 40 + (math.sqrt(3) * Mg / 2)* 3.6
    xanion = 40 + 360 + 100 + (Cl + SO4 / 2) * 3.6
    yanion = 40 + (SO4 * math.sqrt(3) / 2)* 3.6
    xdiam = 0.5 * (xcation + xanion + (yanion - ycation) / math.sqrt(3))
    ydiam = 0.5 * (yanion + ycation + math.sqrt(3) * (xanion - xcation))

    c=np.random.rand(3,1).ravel()
    listagraph=[]
    listagraph.append(plt.scatter(xcation,ycation,zorder=1,c=c, s=60, marker='o', edgecolors='#4b4b4b',label=Label))  # edgecolors='#4b4b4b'
    listagraph.append(plt.scatter(xanion,yanion,zorder=1,c=c, s=60, marker='o', edgecolors='#4b4b4b'))  # edgecolors='#4b4b4b'
    listagraph.append(plt.scatter(xdiam,ydiam,zorder=1,c=c, s=60, marker='o', edgecolors='#4b4b4b'))  # edgecolors='#4b4b4b'
    return listagraph

plt.figure(figsize=(20,15))
plt.imshow(np.flipud(img),zorder=0)
for index, row in datosQuimica.iterrows():
    coordenada(row['Ca_norm'],row['Mg_norm'],row['Cl_norm'],row['SO4_norm'],index)
plt.ylim(0,830)
plt.xlim(0,900)
plt.axis('off')
plt.legend(loc='upper right',prop={'size':12}, frameon=False, scatterpoints=1)
    
plt.savefig('./Output/Piper_Analisis_AFQ.png', dpi=400)
plt.savefig('./Output/Piper_Analisis_AFQ.svg')
#plt.savefig('./Output/PiperFuentesHidricas_52_58.pdf')

#############--Código para ordenar e imprimir la cantidad de cada una de--##############    
#############--las facies hidroquímicas determinadas según Back 1966.--#################
#############--También agrega columnas de hidrofacies e hidrofacies  --#################
#############--resumen al DataFrame que se usará para generar poligonos--###############

hidrofacies_list = ["Bicarbonatada Calcica", "Bicarbonatada Cloruro Calcica",
               "Cloruro Bicarbonatada Calcica", "Cloruro Calcica",
               "Bicarbonatada Calcico Sodica", "Bicarbonatada Cloruro Calcico Sodica",
               "Cloruro Bicarbonatada Calcico Sodica", "Cloruro Calcico Sodica",
               "Bicarbonatada Sodico Calcica", "Bicarbonatada Cloruro Sodico Calcica",
               "Cloruro Bicarbonatada Sodico Calcica", "Cloruro Sodico Calcica",
               "Bicarbonatada Sodica", "Bicarbonatada Cloruro Sodica",
               "Cloruro Bicarbonatada Sodica", "Cloruro Sodica"]
print()
bicarbonatos = datosQuimica['HCO3_CO3_norm']
sodioK = datosQuimica['Na_K_norm']
print()

muestrasFacies, muestraHidrofacies, muestrasHidroResu = hidrofacies(bicarbonatos, sodioK, nombres, hidrofacies_list)#Función en 'hidrofacies.py'

print_hidrofacies(muestrasFacies, hidrofacies_list)#Función en 'hidrofacies.py'

datosQuimica["Hidrofacies"] = muestraHidrofacies
datosQuimica["Hidrofacies_res"] = muestrasHidroResu

datosQuimica = datosQuimica[['Este','Norte','HCO3','CO3','SO4','Cl', 'Na','K','Ca',
                             'Mg','Hidrofacies','Hidrofacies_res']]
"""
datosQuimica = datosQuimica[['Locacion','Este','Norte','HCO3','CO3','SO4','Cl', 'Na','K','Ca',
                             'Mg','Profundidad','Hidrofacies','Hidrofacies_res']]
"""

"""
datosQuimica = datosQuimica[['Locacion','Este','Norte','HCO3','CO3','SO4','Cl', 'Na','K','Ca',
                             'Mg','Balance_I','Ag', 'Al', 'As','B', 'Ba', 'Be', 'Cd', 'Co', 'Cr',
                             'Cu','Fe','Li', 'Mn', 'Mo', 'Ni', 'Pb', 'Sb', 'Se', 'Sr', 'V',
                             'Zn','F','P', 'NO3', 'NO2', 'Acidez_T','Alcalinidad_T', 'Dureza_T',
                             'Conductividad','PH', 'Temperatura', 'Resistividad','Salinidad_E',
                             'Solidos_D', 'Solidos_S', 'Solidos_T', 'Turbiedad','Hidrofacies',
                             'Hidrofacies_res']]
"""
datosQuimica.to_excel("./Fiona/Analisis_AFQ.xlsx")

print()
print("Se analizaron un total de {} muestras.".format(len(nombres)))