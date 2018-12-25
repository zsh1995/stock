import datetime

import tushareDownload
import talib
import numpy as np

from PriorityQueue import PriorityQueue


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

def calc_max_and_back(macd, price,term = 26):
    pq = PriorityQueue(term, lambda a,b: a == b)
    N = len(macd)
    warn_list = [0 for i in range(N)]
    warn_1_index = []
    for i in range(N):
        pq.push(macd[i])
        # 在最值后6六天内
        pmax = 0 if len(warn_1_index) == 0 else warn_1_index[-1]
        if pmax + 6 >= i:
            lend = 0 if i - 3 < 0 else i - 3
            if (macd[lend] > macd[i]) != (price[lend] > price[i]):
                warn_list[i] = 2
        if pq.size() >= term :
            if pq.max() == macd[i]:
                warn_list[i] = 1
                warn_1_index.append(i)
                # 回看前3天
                if i >= 3:
                    if (macd[i - 3] > macd[i]) != (price[i - 3] > price[i]):
                        warn_list[i] = 2
            pq.remove(macd[i - term])
    return warn_list

def calc_across(macd_short, macd_long, term = 12):
    N = len(macd_short)
    pre_flag = True
    unacross = [0 for i in range(N)]
    across_day = []
    for i in range(N):
        s = macd_short[i]
        l = macd_long[i]
        crtflag = s > l
        if crtflag != pre_flag:
            across_day.append(i)
        # unacross day is longger than term
        if len(across_day) >= 1 and i - across_day[-1] >= term and crtflag == pre_flag:
            unacross[i] = 1
        # across more than twice in term
        elif len(across_day) >= 2 and i - across_day[-2] <= term:
            unacross[i] = 2
        pre_flag = crtflag
    return unacross

def cross(dif, dea):
    N = len(dif)
    warn_list = [0 for i in range(N)]
    pre = False
    for i in range(N) :
        crt = dif[i] > dea[i]
        if pre != crt :
            warn_list[i] = 2
        pre =  crt
    return warn_list

def calc_max(data_src, term = 26):
    pq = PriorityQueue(term, lambda a, b: a == b)
    N = len(data_src)
    warn_list = [0 for i in range(N)]
    for i in range(N) :
        pq.push(data_src[i])
        if pq.size() >= term:
            if pq.max() == data_src[i]:
                warn_list[i] = 1
            pq.remove(data_src[i - term])
    return warn_list