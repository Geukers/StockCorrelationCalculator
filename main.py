import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import numpy as np


def get_symbols():
    df = pd.read_excel('StockCorrelations.xlsx',
                       sheet_name='Sheet1')
    return df['Symbols'].values
    

if __name__ == '__main__':

    symbols = get_symbols()
    # get_prices(symbols)
    # calculate_correlation()

