from sqlalchemy import create_engine
import tushare as ts
from datetime import *

api = ts.pro_api('c47e14c7e2d18461135f48996657b13a0c3702820c62c18aa383d49b')
# engine = create_engine('mysql+mysqlconnector://root:123456@192.168.8.226/tushare?charset=utf8')


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
def get_share_data(end_data = datetime.strptime("2018-12-31", "%Y-%m-%d")) :
    start_date_term = datetime.strptime("2005-01-01", "%Y-%m-%d")
    end_date_term = datetime.strptime("2005-12-31", "%Y-%m-%d")
    pre_data = None
    while start_date_term < end_data:
        df = ts.pro_bar(pro_api=api,
                        ts_code='000300.sh',
                        asset='I', freq='D',
                        start_date=toString(start_date_term),
                        end_date=toString(end_date_term))
        df = df[['close', 'trade_date', 'open', 'high', 'low']][::-1]
        if pre_data is None:
            pre_data = df
        else:
            pre_data = pre_data.append(df)
        pre_year = start_date_term.year
        start_date_term = start_date_term.replace(year=pre_year + 1)
        end_date_term = end_date_term.replace(year=pre_year + 1)
    return pre_data