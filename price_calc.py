import tushareDownload

_history_data = None

class price_state:
    def __init__(self):
        self.shake = 0 # 是否震荡
        self.rate = 0 # 震幅百分比 0 - 1
        self.ocrate = 0
        self.hlrate = 0
        self.averange24hl = 0
        self.averange24oc = 0
        self.averange24sh = 0
        self.date = ""

def loal_data():
    global _history_data
    if _history_data is None:
        _history_data = tushareDownload.get_share_data()
    return _history_data

def calc_shake():
    data = loal_data()
    date = data['trade_date']
    list = []
    pre_min =  0
    sum_hl = 0
    sum_oc = 0
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
        # 加入当天
        sum_hl = sum_hl + state.hlrate
        sum_oc = sum_oc + state.ocrate
        sum_shake =  sum_shake + state.rate
        term = 24
        if i >= term:
            # 移除
            sum_hl = sum_hl - list[i - term].hlrate
            sum_oc = sum_oc - list[i - term].ocrate
            sum_shake = sum_shake - list[i - term].rate

            # 计算均值
            state.averange24_hl = sum_hl / term
            state.averange24_oc = sum_oc / term
            state.averange24_sh = sum_shake / term

        if state.rate < 50:
            state.shake = 1
        if state.rate < pre_min:
            pre_min = state.rate
            state.shake = 1
        list.append(state)
    return list


