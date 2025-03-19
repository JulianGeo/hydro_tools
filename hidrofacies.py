# Esta función permite guardar en una lista, las listas con las muestras (nombres) de cada una 
# de las hidrofacies determinadas para las muestras analizadas.
def hidrofacies(bicarbonatos, sodioK, nombres, hidrofacies_list):
    muestrasFacies = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    muestrasHidrofacies = [] #Lista de hidrofacies por cada muestra.
    muestrasHidroResu = [] #Lista de hidrofacies resumidas (4 grupos).
    for i in range(len(bicarbonatos)):
        if (bicarbonatos.iloc[i] > 90 and sodioK.iloc[i] < 10):
            muestrasFacies[0].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[0])
            muestrasHidroResu.append(hidrofacies_list[0])
        if (bicarbonatos.iloc[i] > 50 and bicarbonatos.iloc[i] < 90) and (sodioK.iloc[i] < 10):
            muestrasFacies[1].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[1])
            muestrasHidroResu.append(hidrofacies_list[0])
        if (bicarbonatos.iloc[i] > 10 and bicarbonatos.iloc[i] < 50) and (sodioK.iloc[i] < 10):
            muestrasFacies[2].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[2])
            muestrasHidroResu.append(hidrofacies_list[3])
        if (bicarbonatos.iloc[i] < 10 and sodioK.iloc[i] < 10):
            muestrasFacies[3].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[3])
            muestrasHidroResu.append(hidrofacies_list[3])
        if (bicarbonatos.iloc[i] > 90) and (sodioK.iloc[i] > 10 and sodioK.iloc[i] < 50):
            muestrasFacies[4].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[4])
            muestrasHidroResu.append(hidrofacies_list[0])
        if (bicarbonatos.iloc[i] > 50 and bicarbonatos.iloc[i] < 90) and (sodioK.iloc[i] > 10 and sodioK.iloc[i] < 50):
            muestrasFacies[5].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[5])
            muestrasHidroResu.append(hidrofacies_list[0])
        if (bicarbonatos.iloc[i] > 10 and bicarbonatos.iloc[i] < 50) and (sodioK.iloc[i] > 10 and sodioK.iloc[i] < 50):
            muestrasFacies[6].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[6])
            muestrasHidroResu.append(hidrofacies_list[3])
        if (bicarbonatos.iloc[i] < 10) and (sodioK.iloc[i] > 10 and sodioK.iloc[i] < 50):
            muestrasFacies[7].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[7])
            muestrasHidroResu.append(hidrofacies_list[3])
        if (bicarbonatos.iloc[i] > 90) and (sodioK.iloc[i] > 50 and sodioK.iloc[i] < 90):
            muestrasFacies[8].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[8])
            muestrasHidroResu.append(hidrofacies_list[12])
        if (bicarbonatos.iloc[i] > 50 and bicarbonatos.iloc[i] < 90) and (sodioK.iloc[i] > 50 and sodioK.iloc[i] < 90):
            muestrasFacies[9].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[9])
            muestrasHidroResu.append(hidrofacies_list[12])
        if (bicarbonatos.iloc[i] > 10 and bicarbonatos.iloc[i] < 50) and (sodioK.iloc[i] > 50 and sodioK.iloc[i] < 90):
            muestrasFacies[10].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[10])
            muestrasHidroResu.append(hidrofacies_list[15])
        if (bicarbonatos.iloc[i] < 10) and (sodioK.iloc[i] > 50 and sodioK.iloc[i] < 90):
            muestrasFacies[11].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[11])
            muestrasHidroResu.append(hidrofacies_list[15])
        if (bicarbonatos.iloc[i] > 90 and sodioK.iloc[i] > 90):
            muestrasFacies[12].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[12])
            muestrasHidroResu.append(hidrofacies_list[12])
        if (bicarbonatos.iloc[i] > 50 and bicarbonatos.iloc[i] < 90) and (sodioK.iloc[i] > 90):
            muestrasFacies[13].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[13])
            muestrasHidroResu.append(hidrofacies_list[12])
        if (bicarbonatos.iloc[i] > 10 and bicarbonatos.iloc[i] < 50) and (sodioK.iloc[i] > 90):
            muestrasFacies[14].append(nombres[i])
            muestrasHidrofacies.append(hidrofacies_list[14])
            muestrasHidroResu.append(hidrofacies_list[15])
        if (bicarbonatos.iloc[i] < 10) and (sodioK.iloc[i] > 90):
            muestrasFacies[15].append(nombres[i])   
            muestrasHidrofacies.append(hidrofacies_list[15])
            muestrasHidroResu.append(hidrofacies_list[15])
    return muestrasFacies, muestrasHidrofacies, muestrasHidroResu

# Esta función imprime en consola las listas de las hidrofacies determinadas (nombres)
# y guarda un archivo .txt el resultado impreso en la consola.

def print_hidrofacies(muestrasFacies,hidrofacies_list):
    f = open("Hidrofacies_muestras_octubre_2022.txt", "w")
    for i in range(len(muestrasFacies)):
        if len(muestrasFacies[i]) > 0: 
            print("Hay {} facies de tipo {}.".format(len(muestrasFacies[i]), hidrofacies_list[i]))
            f.write("Hay {} facies de tipo {}.".format(len(muestrasFacies[i]), hidrofacies_list[i]) + "\n")
            print(muestrasFacies[i])
            for j in muestrasFacies[i]:
                f.write(j + ", ")
            f.write("\n")
    f.close()

def coordenadas_iones(datosQuimica, dist_este, dist_norte, precision):
    for row in datosQuimica:
        datosQuimica["Este_Na"] = round(datosQuimica["Este"] - (dist_este * (datosQuimica["Na_meq"] + datosQuimica["K_meq"])),precision)
        datosQuimica["Norte_Na"] = round((datosQuimica["Norte"] + dist_norte),precision)
        datosQuimica["Este_Ca"] = round((datosQuimica["Este"] - (dist_este * datosQuimica["Ca_meq"])),precision)
        datosQuimica["Norte_Ca"] = datosQuimica["Norte"]
        datosQuimica["Este_Mg"] = round((datosQuimica["Este"] - (dist_este * datosQuimica["Mg_meq"])),precision)
        datosQuimica["Norte_Mg"] = round((datosQuimica["Norte"] - dist_norte),precision)
        datosQuimica["Este_SO4"] = round((datosQuimica["Este"] + (dist_este * datosQuimica["SO4_meq"])),precision)
        datosQuimica["Norte_SO4"] = round((datosQuimica["Norte"] - dist_norte),precision)
        datosQuimica["Este_HCO3"] = round((datosQuimica["Este"] + (dist_este * (datosQuimica["HCO3_meq"] + datosQuimica["CO3_meq"]))),precision)
        datosQuimica["Norte_HCO3"] = datosQuimica["Norte"]
        datosQuimica["Este_Cl"] = round((datosQuimica["Este"] + (dist_este * datosQuimica["Cl_meq"])),precision)
        datosQuimica["Norte_Cl"] = round((datosQuimica["Norte"] + dist_norte),precision)
    return datosQuimica