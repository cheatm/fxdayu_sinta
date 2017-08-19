from fxdayu_data.handler.mongo_handler import read, write
from pymongo import MongoClient
import pandas as pd


client = MongoClient("192.168.0.102")
db = client['adjust']


def start(s):
    return s.index[0].replace(hour=0, minute=0)


def end(s):
    return s.index[-1]


mapper = {"start": start, "end": end}


def coder(code):
    return '.'.join(code.split("_"))


def write_adjust(code, s):
    adj = s.groupby(s).agg(mapper)
    adj['adjust'] = adj.index
    print code
    write(db[coder(code)], adj)


adjust = read(client['adjust']['after'])


for code, item in adjust.iteritems():
    try:
        write_adjust(code, item)
    except Exception as e:
        print code, e

