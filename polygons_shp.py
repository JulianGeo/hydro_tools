# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 13:19:07 2023

@author: Chiky
"""

import pandas as pd
import numpy as np

from hidrofacies import coordenadas_iones

iones = {
'HCO3': 61, 'CO3' : 30, 'Cl' : 35, 'SO4': 48,
'Na' : 23, 'Ca' : 20, 'Mg' : 12, 'K'  : 39
}

datosQuimica = pd.read_excel("./Fiona/AFQ_Garzas-12.xlsx")

numero_muestras = len(datosQuimica)#Se necesita antes de multiplicar las muestras.

datosQuimica = datosQuimica.set_index(['ID'])

for ion in iones.keys():
    datosQuimica[str(ion)+'_meq'] = round(datosQuimica[ion]/iones[ion],5)
    
#datosQuimica.to_csv("./Fiona/transformados_a_meq.csv")
print(list(datosQuimica))
muestras = datosQuimica[['Estacion','Este','Norte','HCO3','CO3','SO4','Cl','Na','K','Ca',
                         'Mg','Profundidad','Hidrofacies','Hidrofacies_res']]

"""
muestras = datosQuimica[['Locacion','Este','Norte','HCO3','CO3','SO4','Cl', 'Na','K','Ca',
                             'Mg','Balance_I','Ag', 'Al', 'As','B', 'Ba', 'Be', 'Cd', 'Co','Cr',
                             'Cu', 'Fe','Li', 'Mn', 'Mo', 'Ni', 'Pb', 'Sb', 'Se', 'Sr', 'V','Zn', 
                             'F','P', 'NO3', 'NO2', 'Acidez_T','Alcalinidad_T', 'Dureza_T',
                             'Conductividad', 'PH', 'Temperatura', 'Resistividad','Salinidad_E',
                             'Solidos_D', 'Solidos_S', 'Solidos_T', 'Turbiedad','Hidrofacies',
                             'Hidrofacies_res']]
"""


muestras.to_csv('./Fiona/AFQ_Garzas-12.csv')#Para crear shapefile o cualquiera.

dist_este = 10 # 0.002239 segundos son aproximadamente 250m
dist_norte = 750 # 0.004481 segundos son aproximadamente 500m
precision = 2

# Función en 'hidrofacies.py' que da coordenadas a los iones de los diagramas STIFF.
datosQuimica = coordenadas_iones(datosQuimica,dist_este,dist_norte,precision)

reps = [6 for row in range(len(datosQuimica))]#Genera lista de números 6 para repetir filas.

datosQuimica = datosQuimica.loc[np.repeat(datosQuimica.index.values, reps)]
#datosQuimica.to_csv('./Fiona/prueba.csv')
iones_vertices = ["Na","Ca","Mg","SO4","HCO3","Cl"]
datosQuimica["Iones"] = iones_vertices * numero_muestras#Genera columna de Iones para referenciar.

estes = ["Este_Na","Este_Ca","Este_Mg","Este_SO4","Este_HCO3","Este_Cl"]
nortes = ["Norte_Na","Norte_Ca","Norte_Mg","Norte_SO4","Norte_HCO3","Norte_Cl"]

#Genera DataFrames para asignar coordenadas a los Iones del diagrama de STIFF.
for i in range(len(iones_vertices)):
    selection = datosQuimica[datosQuimica["Iones"] == iones_vertices[i]]
    selection["Este"] = selection[estes[i]]
    selection["Norte"] = selection[nortes[i]]
    selection["Iones_index"] = i
    selection.to_csv('./Fiona/DataframesIones/'+str(iones_vertices[i])+'.csv')

#Se cargan los DataFrame generados anteriormente.       
sodio = pd.read_csv('./Fiona/DataframesIones/Na.csv')
calcio = pd.read_csv('./Fiona/DataframesIones/Ca.csv')
magnesio = pd.read_csv('./Fiona/DataframesIones/Mg.csv')
sulfatos = pd.read_csv('./Fiona/DataframesIones/SO4.csv')
bicarbonatos = pd.read_csv('./Fiona/DataframesIones/HCO3.csv')
cloruros = pd.read_csv('./Fiona/DataframesIones/Cl.csv')

#Se une el DataFrame que se usará para generar el shapefile o otro archivo con Fiona.
datosQuimica = pd.concat([sodio,calcio,magnesio,sulfatos,bicarbonatos,cloruros])

datosQuimica = datosQuimica[['ID','Estacion', 'Este', 'Norte', 'HCO3', 'CO3', 'SO4', 'Cl', 
                                  'Na', 'K','Ca', 'Mg','Profundidad','Hidrofacies','Hidrofacies_res','Iones_index']]
datosQuimica = datosQuimica.set_index(["ID"])

datosQuimica = datosQuimica.sort_values(by=["ID","Iones_index"])

datosQuimica.to_csv('./Fiona/AFQ_Garzas-12_poligonos.csv',encoding='utf-8')#utf-8 es por defecto pero no me guarda bien los acentos y la ñ
                                                                               #latin-1 supuestamente comserva acentos y la ñ.