import requests

import apimoex
import pandas as pd

import datetime
import pandas_datareader
sdate = datetime.datetime(2023,10,31)
edate = datetime.datetime.today()
code = 'GAZP'
data = pandas_datareader.DataReader(code, 'moex', start=sdate, end=edate)
print(data[['OPEN', 'HIGH', 'LOW', 'CLOSE']].tail(10))
data[['OPEN', 'HIGH', 'LOW', 'CLOSE']].plot()
#
# with requests.Session() as session:
#     data = apimoex.get_board_history(session, 'SNGSP')
#     df = pd.DataFrame(data)
#     df.set_index('TRADEDATE', inplace=True)
#     print(df.head(), '\n')
#     print(df.tail(), '\n')
#     df.info()