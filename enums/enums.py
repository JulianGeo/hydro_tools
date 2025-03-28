from enum import Enum

class data_type_enum(Enum):
    TERMAL = 'TERMAL'
    POZO = 'POZO'


#for data in (data_type_enum):
    #print(data.value,"-",data)

#print(data_type_enum.TERMAL.name)


class thermal_columns_enum(Enum):
    T = 'T'
