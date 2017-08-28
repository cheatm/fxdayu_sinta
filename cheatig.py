# from bcolz.ctable import ctable
from fxdayu_data.data_api.blp_reader import BLPTable, MapTable
from datetime import datetime, timedelta
import pandas as pd
from pymongo import MongoClient


def num2date(num):
    return datetime.strptime(str(num), "%Y%m%d000000")


def handle(frame):
    return pd.DataFrame({'adjust': frame['ex_cum_factor']})

table = MapTable("E:\\rqalpha\\bundle\\ex_cum_factor.bcolz", 'start_date', blp2index=num2date)
print len(table.line_map.keys())
# print handle(table.read('000001.XSHE'))

# from rqalpha.data.base_data_source import BaseDataSource
# from rqalpha.data.data_proxy import DataProxy
# from datetime import datetime


# ds = BaseDataSource("E:\\rqalpha\\bundle")
# dp = DataProxy(ds)
# dt = datetime.now()
#
# print ds.history_bars(
#     dp.instruments("000001.XSHE"), 50, "1d", ["datetime", "close", "volume"], dt=dt,
#     adjust_orig=dt, adjust_type='post'
# )