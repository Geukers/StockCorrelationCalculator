import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import xlsxwriter
import xlrd

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
    print("\n===================== Errors =======================\n")
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
            try:
                daily_stock_price[stock] = close_price_list
            except ValueError:
                print(stock + ' has not been public long enough, it has been removed')

    print()
    # i1 = 0
    # while i1 < len(daily_stock_price.columns) - 1:
    #     col1 = daily_stock_price.iloc[:, i1]
    #     i2 = i1 + 1
    #     while i2 < len(daily_stock_price.columns):
    #         col2 = daily_stock_price.iloc[:, i2]
    #         print(daily_stock_price.columns[i1] + " : " + daily_stock_price.columns[i2])
    #         print(repr(np.corrcoef(np.array(col1).astype(np.float), np.array(col2).astype(np.float))))
    #         i2 = i2 + 1
    #     i1 = i1 + 1

    # print(daily_stock_price)

    # print(np.array(daily_stock_price))

    print("\n================ Graph Correlations ================\n")

    array = np.vstack((daily_stock_price.iloc[:, 0].astype(np.float), (daily_stock_price.iloc[:, 1].astype(np.float))))
    # print(array)

    for i in range(2, len(daily_stock_price.columns)):

        # print((daily_stock_price[col]).astype(np.float))
        # print('askdjhfasdfkljhasdfhjklfasdkhjlafsdhkjladfshkjlfskhdjl')
        # array = np.array([array], (daily_stock_price[col]).astype(np.float).tolist())

        array = np.vstack((array, daily_stock_price.iloc[:, i].astype(np.float).tolist()))

        # array = array[..., daily_stock_price.iloc[:, i].astype(np.float).tolist()]


    # print(array)

    print(daily_stock_price.columns.tolist())
    correlation = np.corrcoef(array)
    print(correlation)

    print("\n============ Individual Correlations ==============\n")
    i1 = 0
    while i1 < len(daily_stock_price.columns) - 1:
        col1 = daily_stock_price.iloc[:, i1]
        i2 = i1 + 1
        while i2 < len(daily_stock_price.columns):
            col2 = daily_stock_price.iloc[:, i2]
            print(daily_stock_price.columns[i1] + " : " + daily_stock_price.columns[i2])
            print(repr(np.corrcoef(np.array(col1).astype(np.float), np.array(col2).astype(np.float))))
            i2 = i2 + 1
        i1 = i1 + 1

    # workbook = xlsxwriter.Workbook('StockCorrelations.xlsx')
    # worksheet = workbook.add_worksheet(name="Correlations")
    #
    # row = 0
    #
    # for col, data in enumerate(correlation):
    #     worksheet.write_column(row, col, data)
    #
    # workbook.close()

    # df = get_excel_data()
    # get_prices(data)
    # calculate_correlation()
