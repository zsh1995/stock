import tushareDownload
import talib
import numpy as np
_history_data = None

def load_data():
    global _history_data
    if _history_data is None:
        _history_data = tushareDownload.get_share_data()
    return _history_data

def calc_macd():
    data = load_data()
    m, s, h = talib.MACD(data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    m = np.nan_to_num(m, 0)
    s = np.nan_to_num(s, 0)
    h = np.nan_to_num(h, 0)

    return m,s,h,data['trade_date']