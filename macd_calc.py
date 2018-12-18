import datetime

import tushareDownload
import talib
import numpy as np

def load_data():
    _history_data = tushareDownload.get_share_data(end_data=datetime.datetime.today().strftime("%Y-%m-%d"))
    return _history_data

def calc_macd():
    data = load_data()
    m, s, h = talib.MACD(data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    m = np.nan_to_num(m, 0)
    s = np.nan_to_num(s, 0)
    h = np.nan_to_num(h, 0)

    return m,s,h,data['trade_date']