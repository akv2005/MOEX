import requests
import apimoex
import logging
import pandas as pd
import datetime



logging.basicConfig(level=logging.INFO, filemode='w', filename='py.log',
                    format='%(asctime)s | %(levelname)s | %(message)s')
def fetch_stock_data(ticker, period='24'):
    security = ticker
    start_date = '2024-08-01'  # Начальная дата
    end_date = datetime.datetime.today()  # Конечная дата
    interval = '24' #'24'  Интервал: '1d', '1h', '30m' и т.д.
    with requests.Session() as session:
        stock = apimoex.get_board_candles(session, security=security, start=start_date, end=end_date, interval = interval)
        data = pd.DataFrame(stock)
        return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    """
    :param data: Принимает БД с данными по запрошенной акции
    :return: Возвращает среднее значение колонки 'CLOSE'
    """
    avg = data['close'].mean(axis=0)
    logging.info(f'средняя цена закрытия акций: {avg}')
    return avg


def notify_if_strong_fluctuations(data, threshold=20):
    """

    :param data: Принимает БД с данными по запрошенной акции
    :param threshold: Принимает пороговое значение колебаний в процентах от средней цены цены закрытия за указанный период
    :return: Возвращает предупреждение, если цена закрытия акций за заданный перуд изменяется больше значения threshold
    """
    min_price = data['close'].min()
    max_price = data['close'].max()

    dif = max_price - min_price
    percent = dif / (calculate_and_display_average_price(data) / 100)
    if percent >= threshold:
        logging.warning('высокий уровень колебания акций!')
        return 'Компания не стабильна, будьте внимательны!'


def calculate_rsi(data, window=14):
    """
    Рассчитывает индекс относительной силы (RSI) для данных о ценах акций.

    :param data: DataFrame с историческими данными о ценах акций
    :param window: Период расчета RSI
    :return: DataFrame с добавленным столбцом 'RSI'
    """
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Рассчитывает Moving Average Convergence Divergence (MACD) для данных о ценах акций.

    :param data: DataFrame с историческими данными о ценах акций
    :param short_window: Период для короткой экспоненциальной скользящей средней (EMA)
    :param long_window: Период для длинной экспоненциальной скользящей средней (EMA)
    :param signal_window: Период для сигнальной линии MACD
    :return: DataFrame с добавленными столбцами 'MACD' и 'Signal'
    """
    data['EMA_short'] = data['close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_long'] = data['close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA_short'] - data['EMA_long']
    data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data
