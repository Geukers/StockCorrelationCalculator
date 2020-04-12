import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

import numpy as np
from datetime import datetime, timezone, timedelta
import csv
import requests

if __name__ == '__main__':
    df = pd.read_excel('StockCorrelations.xlsx', sheet_name='Sheet1')

    period2_date_time = datetime.today()
    period1_date_time = period2_date_time - timedelta(days=365)

    period2_unix_timestamp = repr(int(period2_date_time.replace(tzinfo=timezone.utc).timestamp()))
    period1_unix_timestamp = repr(int(period1_date_time.replace(tzinfo=timezone.utc).timestamp()))

    daily_stock_price = pd.DataFrame()
    daily_stock_price = daily_stock_price.reindex(columns=df['Symbols'])

    for stock in df['Symbols']:
        CSV_URL = 'https://query1.finance.yahoo.com/v7/finance/download/' + stock + \
                  '?period1=' + period1_unix_timestamp + \
                  '&period2=' + period2_unix_timestamp + \
                  '&interval=1d' \
                  '&events=history'

        with requests.Session() as s:
            download = s.get(CSV_URL)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            my_list.pop(0)

            close_price_list = []

            for close_price in my_list:
                close_price_list.append(close_price[4])

            daily_stock_price[stock] = close_price_list

    # i1 = 0
    # while i1 < daily_stock_price.size() - 1:
    #     col1 = daily_stock_price.iloc[i1, :]
    #     i2 = i1+1
    #     while i2 < daily_stock_price.size():



    # df = get_excel_data()
    # get_prices(data)
    # calculate_correlation()
