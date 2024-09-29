import pandas as pd
import apimoex
import requests

# Инициализируем API


# Задаем параметры для получения свечей
security  = 'SBER'  # Здесь укажите нужный тикер
start_date = '2024-01-01'  # Начальная дата
end_date = '2024-09-01'    # Конечная дата
interval = '24'            # Интервал: '1d', '1h', '30m' и т.д.

# Получаем данные
with requests.Session() as session:
    candles = apimoex.get_board_candles(session, security=security, start=start_date, end=end_date, interval = interval)
    #Преобразуем в DataFrame
    df = pd.DataFrame(candles)
    print(df)

# Выводим данные
print(df)

# import requests
#
# import apimoex
# import pandas as pd
#
#
# request_url = ('https://iss.moex.com/iss/engines/stock/'
#                'markets/shares/boards/TQBR/securities.json')
# arguments = {'securities.columns': ('SECID,'
#                                     'REGNUMBER,'
#                                     'LOTSIZE,'
#                                     'SHORTNAME')}
# with requests.Session() as session:
#     iss = apimoex.ISSClient(session, request_url, arguments)
#     data = iss.get()
#     df = pd.DataFrame(data['securities'])
#     df.set_index('SECID', inplace=True)
#     print(df.head(), '\n')
#     print(df.tail(), '\n')
#     df.info()