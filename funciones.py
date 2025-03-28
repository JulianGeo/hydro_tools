from setup.config import *
from variables import *
from enums.enums import *

def diagramaStiff(ion_data, maxConNorm, index, has_labels=True, color=facecolor):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection

    fig, ax = plt.subplots(figsize=(26,13))  # figsize=(14,7)# Modifiqué el tamaño de salida de la figura
    patches = []

    polygon = Polygon(ion_data, closed= True) 
    patches.append(polygon)

    p = PatchCollection(
        patches, 
        facecolor=color, 
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

def get_stiff_color(fixed_color, data_type, row):
    """
    Get the color for the Stiff diagram based on the fixed color and data type.

    Args:
        fixed_color (str): The fixed color for the Stiff diagram.
        data_type (str): The type of data ('cationes' or 'aniones').
        column_name (str): The name of the column to determine the color.

    Returns:
        str: The color for the Stiff diagram.
    """
    if fixed_color:
        return facecolor
    elif data_type == data_type_enum.TERMAL.value:
        return get_stiff_thermal_colors(row)
    else:
        return facecolor 
    

def get_stiff_thermal_colors(row):
    """
    Get the color for the Stiff diagram based on the thermal data.

    Args:
        row (pd.Series): The row of data to determine the color.

    Returns:
        str: The color for the Stiff diagram.
    """

    if thermal_columns_enum.T.value not in row.index:
        raise ValueError(f"Column '{thermal_columns_enum.T.value}' does not exist in the DataFrame.")
    
    if row[thermal_columns_enum.T.value] < 25:
        return '#1831e8'  # Dark blue
    elif row[thermal_columns_enum.T.value] < 35:
        return '#18bfe8'  # Light blue
    elif row[thermal_columns_enum.T.value] < 45:
        return '#1be818'  # Light green 
    elif row[thermal_columns_enum.T.value] < 55:
        return '#fff419'  # Yellow
    elif row[thermal_columns_enum.T.value] < 65:
        return '#f89505'  # Orange
    elif row[thermal_columns_enum.T.value] < 75:
        return '#f83105'  # Red
    else:
        return '#f805de' # Purple