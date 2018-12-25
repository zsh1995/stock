from sqlalchemy import create_engine
import tushare as ts
from datetime import *
import pandas as pd
import threading
from functools import lru_cache
from flask import current_app

api = ts.pro_api('c47e14c7e2d18461135f48996657b13a0c3702820c62c18aa383d49b')
# engine = create_engine('mysql+mysqlconnector://root:123456@192.168.8.226/tushare?charset=utf8')
R = threading.Lock()
# today = datetime.today()
#today = datetime.strptime("2008-01-01", "%Y-%m-%d")
def toString(date):
    return date.strftime('%Y%m%d')
# while start_date_term < today :
#     df = ts.pro_bar(pro_api = api,
#                     ts_code='000300.sh',
#                     asset='I', freq='D',
#                     start_date=toString(start_date_term),
#                     end_date=toString(end_date_term))
#     pre_year = start_date_term.year
#     start_date_term = start_date_term.replace(year=pre_year + 1)
#     end_date_term = end_date_term.replace(year=pre_year + 1)
    # print(toString(end_date))
    #追加数据到现有表
    #df.to_sql('sh000001',engine,if_exists='append')
    #print(df['close'][0])
def get_share_data(end_data = "2018-12-31", freq = 'D') :
    global test
    current_app.logger.debug('test value is :' + test)
    needLock = test != end_data
    try:
        if needLock:
            R.acquire()
        df = _get_share_data(end_data, freq)
    finally:
        if needLock:
            R.release()
    return df

test = ""
def _get_share_data(end_data = "2018-12-31", freq = 'D') :
    global test
    daily_data = _get_index_data(end_data = end_data)
    data = None
    if freq == 'D':
        data = daily_data
    elif freq == 'W':
        daily_data['index_date'] = pd.to_datetime(daily_data['trade_date'])
        daily_data = daily_data.set_index(['index_date'])
        rdf = daily_data.resample('W').agg({
            'close': lambda r: r.tail(1),
            'open': lambda r: r.head(1),
            'high': 'max',
            'low': 'min',
            'trade_date': lambda r: r.tail(1),
        })
        rdf = rdf.dropna(axis=0)
        rdf = rdf.reset_index(drop=False)
        # rdf['trade_date'] = rdf['trade_date'].apply(lambda x: datetime.strftime(x,"%Y-%m-%d"))
        data = rdf
    test = end_data
    return data

@lru_cache(maxsize=20)
def _get_index_data(from_data = '2005-01-01', end_data = '2018-12-31'):
    end_data = datetime.strptime(end_data, "%Y-%m-%d")
    start_date_term = datetime.strptime("2005-01-01", "%Y-%m-%d")
    end_date_term = datetime.strptime("2005-12-31", "%Y-%m-%d")
    pre_data = None
    while start_date_term < end_data:
        df = ts.pro_bar(pro_api=api,
                        ts_code='000300.sh',
                        asset= 'I',
                        freq='D',
                        start_date=toString(start_date_term),
                        end_date=toString(end_date_term))
        if df is None :
            raise Exception('date from %s -> %s is null'% (start_date_term, end_date_term))
        df = df[::][::-1]
        # df = df[['close', 'trade_date', 'open', 'high', 'low']][::-1]
        if pre_data is None:
            pre_data = df
        else:
            pre_data = pre_data.append(df)
        pre_year = start_date_term.year
        start_date_term = start_date_term.replace(year=pre_year + 1)
        end_date_term = end_date_term.replace(year=pre_year + 1)
    return pre_data

# 废弃
def general_data(start_date, end_date, asset, freq, ts_code):
    df = ts.pro_bar(pro_api = api,
                    ts_code=ts_code,
                    asset=asset,
                    freq='D',
                    start_date=start_date,
                    end_date=end_date)
    if freq == 'W':
        df['index_date'] = pd.to_datetime(df['trade_date'])
        df = df.set_index(['index_date'])
        rdf = df.resample('W').agg({
            'close':lambda r: r.tail(1),
            'open':lambda r: r.head(1),
            'high':'max',
            'low':'min',
            'trade_date': lambda r: r.tail(1),
        })
        rdf = rdf.dropna(axis=0)
        rdf = rdf.reset_index(drop=False)
        # rdf['trade_date'] = rdf['trade_date'].apply(lambda x: datetime.strftime(x,"%Y-%m-%d"))
        return rdf
    else :
        if df is None :
            raise Exception('date from %s -> %s is null'% (start_date, end_date))
        return df[::][::-1]