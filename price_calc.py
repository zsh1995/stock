import datetime

import tushareDownload


class price_state:
    def __init__(self):
        self.shake = 0 # 是否震荡
        self.rate = 0 # 震幅百分比 0 - 1
        self.ocrate = 0
        self.hlrate = 0
        self.averange24_hl = 0
        self.averange24_oc = 0
        self.averange24_sh = 0
        self.averange24_co = 0
        self.corate = 0
        self.date = ""

def loal_data(end_date = datetime.datetime.today(),freq = 'D'):
    if freq == 'D':
        _history_data_daily = tushareDownload.get_share_data(end_data=end_date.strftime("%Y-%m-%d"))
        return _history_data_daily
    elif freq == 'W':
        _history_data_weekly = tushareDownload.get_share_data(end_data = end_date.strftime("%Y-%m-%d"), freq='W')
        return _history_data_weekly

def get_trade_date(from_date , to):
    return loal_data(end_date=datetime.datetime.strptime(to, "%Y-%m-%d"))['trade_date'].tolist()

def calc_shake(term = 24, freq = 'D'):
    data = loal_data(freq = freq)
    date = data['trade_date']
    list = []
    pre_min =  0
    sum_hl = 0
    sum_oc = 0
    sum_co = 0
    sum_shake = 0
    for i in range(len(date)):
        state = price_state()
        open = data['open'].iloc[i]
        close = data['close'].iloc[i]
        high = data['high'].iloc[i]
        low = data['low'].iloc[i]
        state.date = date.iloc[i]
        state.ocrate = 1000 * round(abs(open - close) / open, 4)
        state.rate = int(100 * abs(open - close) / (high - low))
        state.hlrate = 1000 * round((high - low) / open, 4)
        pclose = open if i == 0 else data['close'].iloc[i-1]
        state.corate = 1000 * round(abs(pclose - open) / pclose, 4)
        # 加入当天
        sum_hl = sum_hl + state.hlrate
        sum_oc = sum_oc + state.ocrate
        sum_co = sum_co + state.corate
        sum_shake =  sum_shake + state.rate
        if i >= term:
            # 移除
            sum_hl = sum_hl - list[i - term].hlrate
            sum_oc = sum_oc - list[i - term].ocrate
            sum_shake = sum_shake - list[i - term].rate
            sum_co = sum_co - list[i - term].corate

            # 计算均值
            state.averange24_hl = sum_hl / term
            state.averange24_oc = sum_oc / term
            state.averange24_sh = sum_shake / term
            state.averange24_co = sum_co / term

        if state.rate < 50:
            state.shake = 1
        if state.rate < pre_min:
            pre_min = state.rate
            state.shake = 1
        list.append(state)
    return list


