from funciones import *
from setup.config import *
import pandas as pd

datosQuimica = pd.read_excel(chem_data_path)


datosQuimicaMeq = calculo_milieq(datosQuimica)
datosQuimicaBal = calculo_balance_ionico(datosQuimicaMeq)

datosQuimicaBal.to_csv(chem_data_output_path, index=False)
