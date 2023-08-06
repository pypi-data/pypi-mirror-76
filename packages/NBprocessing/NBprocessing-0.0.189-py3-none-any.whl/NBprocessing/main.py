from categorical import NBcategorical
from continuous import NBcontinuous
from plot import NBplot
from general import NBgeneral
import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv('dataset_cars.csv')
    print(data.columns)
    print(NBgeneral.missing_values(data))

