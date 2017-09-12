import six
import pandas as pd
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import MongoClient
from pymongo import UpdateOne
from functools import partial


def create_client(**config):
    users = config.pop("users", {})
    client = MongoClient(**config)
    auth(client, users)
    return client


def create_filter(index, start, end, length, kwargs):
    index_range = {}
    if start:
        index_range["$gte"] = start
    else:
        kwargs.setdefault('sort', []).append((index, -1))
    if end:
        index_range["$lte"] = end
    if length:
        kwargs['limit'] = length
    if len(index_range):
        kwargs.setdefault('filter', {})[index] = index_range
    return kwargs


def auth(client, users):
    if isinstance(users, six.string_types):
        import json
        users = json.load(open(users))

    for db_name, config in users.items():
        client[db_name].authenticate(**config)


def normalize(data, index=None):
    if isinstance(data, pd.DataFrame):
        if index and (index not in data.columns):
            data[index] = data.index
        return [doc[1].to_dict() for doc in data.iterrows()]
    elif isinstance(data, dict):
        key, value = list(map(lambda *args: args, *data.items()))
        return list(map(lambda *args: dict(map(lambda x, y: (x, y), key, args)), *value))
    elif isinstance(data, pd.Series):
        if data.name is None:
            raise ValueError('name of series: data is None')
        name = data.name
        if index is not None:
            return list(map(lambda k, v: {index: k, name: v}, data.index, data))
        else:
            return list(map(lambda v: {data.name: v}, data))
    else:
        return data


def read(collection, index='datetime', start=None, end=None, length=None, **kwargs):
    if isinstance(collection, Collection):
        if index:
            kwargs = create_filter(index, start, end, length, kwargs)

        if index:
            if 'sort' not in kwargs:
                kwargs['sort'] = [(index, 1)]
        data = list(collection.find(**kwargs))

        for key, value in kwargs.get('sort', []):
            if value < 0:
                data.reverse()
        data = pd.DataFrame(data)

        if len(data):
            data.pop('_id')
            if index:
                data.index = data.pop(index)

        return data

    else:
        raise TypeError("Type of db should be %s not %s" % (Collection, type(collection)))


def reads(db, names=None, index='datetime', start=None, end=None, length=None, **kwargs):
    if isinstance(db, Database):
        if names:
            return pd.Panel.from_dict(
                {name: read(db[name], index, start, end, length, **kwargs) for name in names}
            )
        else:
            return pd.Panel.from_dict(
                {name: read(db[name], index, start, end, length, **kwargs) for name in db.collection_names()}
            )
    else:
        raise TypeError("Type of db should be %s not %s" % (Database, type(db)))


def write(collection, data, index=None):
    data = normalize(data, index)
    result = collection.insert_many(data)
    return result


def create_update(up, index, how, upsert):
    return UpdateOne({index: up[index]}, {how: up}, upsert)


def update(collection, data, index="datetime", how='$set', upsert=True):
    if isinstance(collection, Collection):
        data = normalize(data, index)
        result = collection.bulk_write(
            list(map(partial(create_update, index=index, how=how, upsert=upsert), data))
        )
        return result
    else:
        raise TypeError("Type of db should be %s not %s" % (Collection, type(collection)))


def inplace(collection, data, index='datetime'):
    if isinstance(collection, Collection):
        data = normalize(data, index)

        collection.delete_many({index: {'$gte': data[0][index], '$lte': data[-1][index]}})
        collection.insert_many(data)
        return {'collection': collection.name, 'start': data[0], 'end': data[-1]}
    else:
        raise TypeError("Type of db should be %s not %s" % (Collection, type(collection)))