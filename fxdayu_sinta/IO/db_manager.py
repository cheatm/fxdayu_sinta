from fxdayu_sinta.utils.mongo import read, update, auth
from pymongo import DeleteMany, MongoClient
from datetime import datetime, timedelta
from functools import partial
from six import string_types


def create_client(conf):
    users = conf.pop("users", {})
    client = MongoClient(**conf)
    auth(client, users)
    return client


def date_range(date, start=timedelta(), end=timedelta(days=1)):
    if not isinstance(date, datetime):
        date = datetime.strptime(date, "%Y-%m-%d")
    else:
        date = datetime(date.year, date.month, date.hour)
    return {'datetime': {'$gt': date+start, '$lte': date+end}}


market_range = partial(date_range, start=timedelta(hours=9, minutes=30), end=timedelta(hours=15))


def is_in_db(collection, date, count):
    return collection.find(date_range(date)).count().real == count


class StockCollection():

    def __init__(self, collection, unit, frequency=None):
        self.collection = collection
        self.unit = unit
        self.freq = frequency

    def __getitem__(self, date):
        return read(self.collection, filter=date_range(date))

    def exist(self, date):
        return is_in_db(self.collection, date, self.unit)

    def delete(self, date):
        if isinstance(date, string_types) or isinstance(date, datetime):
            return self.collection.delete_many(date_range(date)).deleted_count
        else:
            if len(date):
                return self.collection.bulk_write(
                    [DeleteMany(date_range(d)) for d in date]
                ).deleted_count

    def write(self, data):
        return update(self.collection, data)


class DBManager():

    def __init__(self, client, main, freq):
        self.client = client
        self.main = main
        self.freq = freq

    def freqs(self, code):
        return {freq: self[code, freq] for freq in self.freq}

    def __getitem__(self, item):
        if isinstance(item, tuple):
            freq = self.freq[item[1]]
            return StockCollection(self.client[freq['db']][item[0]], freq['unit'], item[1])
        else:
            return StockCollection(self.client[self.main['db']][item], self.main['unit'])

    @classmethod
    def config(cls, config=None):
        if not config:
            from fxdayu_sinta.IO.config import get_storage

            config = get_storage()['mongo_config']

        return cls(create_client(config['client']), config['main'], config['freq'])

    @classmethod
    def env(cls):
        from fxdayu_sinta.IO.environment import get_env
        from fxdayu_sinta.IO import MONGO

        mongo = get_env()[MONGO]
        return cls(create_client(mongo['client']), mongo['main'], mongo['freq'])
