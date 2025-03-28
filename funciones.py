from setup.config import *
from variables import *
import pandas as pd

def diagramaStiff(a, maxConNorm, index, has_labels=True):
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection


    
    fig, ax = plt.subplots(figsize=(26,13))  # figsize=(14,7)# Modifiqué el tamaño de salida de la figura
    patches = []

    polygon = Polygon(a, closed= True) 
    patches.append(polygon)

    p = PatchCollection(
        patches, 
        facecolor=facecolor, 
        edgecolor=edgecolor, 
        alpha=alpha,
        linewidths=linewidths,
    )

    ax.add_collection(p)

    if has_labels:
        #alteramos los ejes
        x = [0, .125, .25, .375, .5, .625, .75, .875, 1]
        labels = [maxConNorm/2, .75*maxConNorm/2, .5*maxConNorm/2, .25*maxConNorm/2,
                0, .25*maxConNorm/2, .5*maxConNorm/2, .75*maxConNorm/2, maxConNorm/2]
        formattedLabels = ["%.1f" % label for label in labels]
        plt.yticks([0,0.5,1],[0,0.5,1], fontsize=0 )
        plt.xticks(x, formattedLabels, fontsize=40, weight='bold')     # Modifiqué el tamaño de los números en la escala x
        plt.grid(visible=True, which='minor', linestyle='-')
        
        ax.set_title(index,weight='bold', fontsize=50) # Modifiqué estilo de la letra a negrita

        ax.set_xlabel('meq/l', fontsize=40,weight='bold') # Modifiqué estilo de la letra a negrita
        
        

        #Generamos las etiquetas de los cationes
        ax.text(-0.02, 1, 'Na + K', fontsize=50, horizontalalignment='right', weight='bold')  # Modifiqué estilo de la letra a negrita
        ax.text(-0.02, 0.5, 'Ca', fontsize=50, horizontalalignment='right', weight='bold')
        ax.text(-0.02, 0, 'Mg', fontsize=50, horizontalalignment='right', weight='bold')

        #Generamos las etiquetas de los aniones
        ax.text(1.02, 1, 'Cl', fontsize=50,weight='bold')                   # Modifiqué estilo de la letra a negrita
        ax.text(1.02, 0.5, 'HCO3 + CO3', fontsize=50,weight='bold')
        ax.text(1.02, 0, 'SO4', fontsize=50,weight='bold')
    
    else:
        # Remove axes if has_labels is False
        ax.axis('off')

        # Remove white background
        fig.patch.set_visible(False)
        ax.patch.set_visible(False)
    
    plt.close()
    
    return fig


def calculo_milieq(datosQuimica):
    #datosQuimica.head()
    datosQuimicaMeq = datosQuimica.copy()
    for ion in iones.keys():
        datosQuimicaMeq[str(ion)+'_meq'] = datosQuimica[ion]/iones[ion]
    return datosQuimicaMeq

def calculo_balance_ionico(datosQuimica):
    datosQuimica.head()
    datosQuimicaBal = datosQuimica.copy()
    datosQuimicaBal['cationes'] = datosQuimica['Na_meq'] + datosQuimica['K_meq'] + datosQuimica['Ca_meq'] + datosQuimica['Mg_meq']
    datosQuimicaBal['aniones'] = datosQuimica['Cl_meq'] + datosQuimica['HCO3_meq'] + datosQuimica['CO3_meq'] + datosQuimica['SO4_meq']
    datosQuimicaBal['Balance'] = ((datosQuimicaBal['cationes']-datosQuimicaBal['aniones'])*100)/(datosQuimicaBal['cationes']+datosQuimicaBal['aniones'])
    return datosQuimicaBal

def clean_sample_names(df, sample_name='Estacion'):
    """
    Cleans the 'sample_name' column of a Pandas DataFrame by replacing
    specific characters and setting it as the index.

    Args:
        df (pd.DataFrame): The input DataFrame containing a column named 'Estacion'.

    Returns:
        pd.DataFrame: The DataFrame with the cleaned 'sample_name' column as the index.
    """
    if sample_name not in df.columns:
        raise ValueError(f"The DataFrame must contain a column named {sample_name}.")

    df[sample_name] = df[sample_name].str.replace("/", "_")
    df[sample_name] = df[sample_name].str.replace("–", "-")
    df[sample_name] = df[sample_name].str.replace(" |%/s", "", regex=True)  # Added regex=True for clarity
    df[sample_name] = df[sample_name].str.strip()
    return df