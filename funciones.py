from setup.config import *

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
    
    plt.close()
    
    return fig
