from datetime import datetime

import talib
import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
from PriorityQueue import PriorityQueue
import tushareDownload
import  scipy.signal as sgn


class RSISate:
    '''
    '''
    state_map = {
        'LONG_TOP': 6,
        'LONG_BOTTOM': 5,
        'MEDIUM_TOP': 4,
        'MEDIUM_BOTTOM': 3,
        'SHORT_TOP': 2,
        'SHORT_BOTTOM': 1
    }
    unacross_map = {
        19 : 3,
        12 : 2,
        9 : 1,
        0: 0,
    }
    MAX_UNACROSS = 17
    def unacross_rank(unacross_day):
        for i in RSISate.unacross_map:
            if unacross_day >= i:
                return RSISate.unacross_map[i]
        return 0

    def __init__(self):
        self.polar_state = 0
        self.polar_state_rank = 0
        self.across = 0
        self.move = 0
        self.cross = 0
        self.back_trend = 0
        self.shake = 0
    def __str__(self):
        return str(self.polar_state) + " " + str(self.polar_state_rank)
def loal_data():
    _df = tushareDownload.get_share_data(end_data= datetime.today().strftime("%Y-%m-%d"))
    return _df
'''
获取历史开盘和收盘价
'''
def get_histroy_price():
    df = loal_data()
    return df[['open','close','trade_date']]

def get_history_index() :
    df = loal_data()
    tmp = df['close']
    return tmp, df['trade_date']

def rsi_back_calc(price, rsi, rsi_state_list):
    topback, bottomback = rsi_back(price, rsi['rsi6'])
    for i in topback:
        rsi_state_list[i].back_trend = 1
    for i in bottomback:
        rsi_state_list[i].back_trend = 2

def rsi_back(price, rsi):
    iprice = np.array(price)
    irsi = np.array(rsi)
    local_max_rsi = sgn.argrelextrema(irsi, np.greater)[0]
    local_min_rsi = sgn.argrelextrema(irsi, np.less)[0]
    local_max_price = sgn.argrelextrema(iprice, np.greater)[0]
    local_min_price = sgn.argrelextrema(iprice, np.less)[0]
    topback = []
    bottomback = []
    for i in range(1,len(local_max_price)):
        nowaday = local_max_price[i]
        peek_top = iprice[nowaday]
        tmp = i
        prepeekday = nowaday
        while nowaday - prepeekday < 7 and tmp >= 0:
            prepeekday = local_max_price[tmp]
            tmp = tmp - 1
        if tmp < 0:
            continue

        peek_top_pre = iprice[prepeekday]

        if peek_top > peek_top_pre:
            prersipeek_max = local_max_rsi[find_pre_peek(local_max_rsi, nowaday - 7)]
            if irsi[local_max_price[i]] < irsi[prersipeek_max]:
                topback.append(nowaday)

    for i in range(1, len(local_min_price)):
        nowaday = local_min_price[i]
        peek_bottom = iprice[nowaday]

        tmp = i
        prepeekday = nowaday
        while nowaday - prepeekday < 7 and tmp >=0:
            prepeekday = local_min_price[tmp]
            tmp = tmp - 1
        if tmp < 0 :
            continue
        peek_bottom_pre = iprice[prepeekday]

        if peek_bottom < peek_bottom_pre:
            prersipeek_min = local_min_rsi[find_pre_peek(local_min_rsi, nowaday - 7)]
            if irsi[nowaday] > irsi[prersipeek_min]:
                bottomback.append(nowaday)
    return topback,bottomback
'''
bisearch
'''
def find_pre_peek(peeks, index):
    lo = 0
    hi = len(peeks) - 1
    length = len(peeks)
    while lo <= hi:
        mid = int((lo + hi) / 2)
        # print(mid)
        if peeks[mid] < index and (mid + 1 >= length or peeks[mid + 1] >= index):
            return mid
        elif mid + 1 >= length or peeks[mid+1] < index:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def test_find():
    l = [10, 14, 18, 24]
    assert find_pre_peek(l,28), 2

def calc_rsi() :
    nw = {}
    tmp, nw['date'] = get_history_index()

    nw['rsi6'] = np.nan_to_num(talib.RSI(tmp, timeperiod=6), 0).tolist()
    nw['rsi12'] = np.nan_to_num(talib.RSI(tmp, timeperiod=12), 0).tolist()
    nw['rsi24'] = np.nan_to_num(talib.RSI(tmp, timeperiod=24), 0).tolist()
    nw['date'] = nw['date'].tolist()
    # x = np.linspace(0, len(nw['date']))
    # plt.plot(nw['rsi6'])
    # plt.plot(nw['rsi12'])
    # plt.plot(nw['rsi24'])
    # plt.legend()
    # plt.show()
    return nw

def rsi_local_max(rsi, max = True, slider_width = 30):
    list = []
    slider = 0
    SLIDER_WIDTH = slider_width
    pq = PriorityQueue(SLIDER_WIDTH, lambda a, b: a[1] == b[1])
    maxFlag = -1
    if not max:
        maxFlag = 1

    for i in range(len(rsi)):
        list.append(0)
        rsi6 = maxFlag * rsi[i]
        rsitup = (rsi6, i)
        if slider < SLIDER_WIDTH:
            pq.push((rsi6, i))
            slider+=1
        else:
            pq.remove((0,i - SLIDER_WIDTH))
            if pq.push(rsitup) :
                rank = pq.getRank(rsitup, 4)
                if rank <= 3 and rank > 0:
                    # print(rank)
                    list[i] = rank
    return list


def tester():
    list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    print(rsi_local_max(list, True, 3))

# tester()




def _mean(atuple):
    sum = 0
    for i in atuple:
        if i != 0:
            sum += 4 - i
    return sum / len(atuple)


def rsi_local_max_all(rsi, list):
    for i in range(len(rsi['rsi6'])):
        list.append(RSISate())
    res1 = rsi_local_max(rsi['rsi6'], True)
    res2 = rsi_local_max(rsi['rsi12'], True)
    res3 = rsi_local_max(rsi['rsi24'], True)
    cnt = 0
    for t in zip(res1, res2, res3):
        list[cnt].polar_state = int(_mean(t))
        cnt += 1
    res1 = rsi_local_max(rsi['rsi6'], False)
    res2 = rsi_local_max(rsi['rsi12'], False)
    res3 = rsi_local_max(rsi['rsi24'], False)
    cnt = 0
    for t in zip(res1, res2, res3):
        tmp = int(_mean(t))
        if tmp != 0:
            list[cnt].polar_state = tmp + 3
        cnt += 1

def rsi_state(rsi, list):
    interval_map={
        'LONG_TOP':[75,70,65],
         'LONG_BOTTOM':[30,35,39],
         'MEDIUM_TOP': [80,75,70],
         'MEDIUM_BOTTOM':[35,40,45],
         'SHORT_TOP':[90,82,75],
         'SHORT_BOTTOM':[20,25,30]
         }
    type_map = {
        'LONG_TOP': 'rsi24',
        'LONG_BOTTOM': 'rsi24',
        'MEDIUM_TOP': 'rsi12',
        'MEDIUM_BOTTOM': 'rsi12',
        'SHORT_TOP': 'rsi6',
        'SHORT_BOTTOM': 'rsi6'
    }
    for i in range(len(rsi['rsi6'])):
        list.append(RSISate())
    for i in range(len(rsi['rsi6'])):
        for key in interval_map:
            tp = type_map[key]
            interval = interval_map[key]
            rsi_val = rsi[tp][i]
            if interval[0] > interval[1]:
                compare = lambda a,b : a >= b
            else:
                compare = lambda a,b : a <= b
            crtState = list[i]
            if compare(rsi_val, interval[2]):
                crtState.polar_state = RSISate.state_map[key]
                if compare(rsi_val, interval[0]):
                    crtState.polar_state_rank = 3
                elif compare(rsi_val, interval[1]):
                    crtState.polar_state_rank = 2
                else:
                    crtState.polar_state_rank = 1
'''
'''
def short_uncross_long(rsi, list) :
    for i in range(len(list)):
        uncross_count = 0
        bigger = rsi['rsi6'][i] > rsi['rsi24'][i]
        for j in range(1,RSISate.MAX_UNACROSS):
            cmp = rsi['rsi6'][i-j] > rsi['rsi24'][i-j]
            eq = abs(rsi['rsi6'][i-j] - rsi['rsi24'][i-j]) < 0.5
            if (cmp ^ bigger) or eq:
                break
            uncross_count += 1
        list[i].across = RSISate.unacross_rank(uncross_count)

def loca_max_term(rsi, list):
    extreams = sgn.argrelextrema(np.array(rsi['rsi6']), np.greater)
    extreams_bottom = sgn.argrelextrema(np.array(rsi['rsi6']), np.less)
    for i in extreams[0]:
        list[int(i)].move = 1
    for i in extreams_bottom[0]:
        list[int(i)].move = 2



# cList = []
# data = calc_rsi()
# rsi_state(data, cList)
# for tmp in cList:
#     print(tmp)


# np.savetxt('rsi6.js', nw['rsi6'])
# np.savetxt('rsi12.js', nw['rsi12'])
# np.savetxt('rsi24.js', nw['rsi24'])
# print(rsi_6)

# nw['rsi6'].to_json('rsi6.js')
# nw['rsi12'].to_json('rsi12.js')
# nw['rsi24'].to_json('rsi24.js')
# nw['date'].to_json('date.js')

