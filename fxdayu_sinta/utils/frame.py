import pandas as pd
from datetime import datetime
from itertools import chain
from fxdayu_sinta.IO.sina_tick import tick2min
from datetime import timedelta


class TimeEdge():
    def __init__(self, edge):
        self.edge = edge
        self.start = None
        self.end = None

    def range(self, end):
        self.end = end
        self.start = self.edge(end)
        return end

    def __call__(self, x):
        self.range(x[-1])
        return pd.DatetimeIndex(
            reversed(list(map(self.scheduler, reversed(x))))
        )

    def scheduler(self, t):
        if t < self.end and (t > self.start):
            return self.end
        else:
            return self.range(t)


MIN1FACTOR = {'min': 1, 'H': 60, 'D': 240, 'W': 240*5, 'M': 240*5*31}
STOCK_GROUPER = {
    'W': TimeEdge(lambda x: x.replace(hour=0, minute=0)-timedelta(days=x.weekday())),
    'H': TimeEdge(lambda x: x.replace(minute=30, hour=x.hour if x.minute > 30 else x.hour-1) if x.hour < 12
                  else x.replace(minute=0, hour=x.hour if x.minute != 0 else x.hour-1)),
    'D': TimeEdge(lambda t: t.replace(hour=9, minute=30, second=0))
    }

RESAMPLE_MAP = {'high': 'max',
                'low': 'min',
                'close': 'last',
                'open': 'first',
                'volume': 'sum'}


class Resampler(object):

    def __init__(self, grouper=STOCK_GROUPER, factor=MIN1FACTOR):
        self.grouper = grouper
        self.factor = factor

    def resample(self, data, how):
        grouper = self.grouper.get(how, None)
        if grouper:
            return data.groupby(grouper).agg(RESAMPLE_MAP)
        else:
            return data.resample(how, label='right', closed='right').agg(RESAMPLE_MAP).dropna()

    @staticmethod
    def f_period(frequency):
        n = ''
        w = ''
        for f in frequency:
            if f.isdigit():
                n += f
            else:
                w += f

        return (int(n) if len(n) else 1), w

    def expand_length(self, length, frequency):
        n, w = self.f_period(frequency)
        return length*n*self.factor[w]


def expand(*args):
    result = pd.concat(args)
    return result[~result.index.duplicated()].sort_index()


def match(series, value):
    return series[series==value].index


def candle(code, date, frame):
    raw = tick2min(frame)
    if is_sz(code):
        raw = sz_slice(raw)

    return fill_candle(pd.DataFrame(raw, date2index(date)))


def fill_candle(frame):
    if isinstance(frame, pd.DataFrame):
        frame['volume'].fillna(0, inplace=True)
        frame['close'].ffill(inplace=True)
        frame.fillna(
            {"high": frame['close'], 'low': frame['close'], 'open': frame['close']},
            inplace=True
        )
        frame['open'].bfill(inplace=True)
        return frame.fillna(
            {"high": frame['open'], 'low': frame['open'], 'close': frame['open']}
        )
    else:
        raise TypeError("Expected %s for frame not %s" % (type(pd.DataFrame), type(frame)))


def date2index(date):
    date = datetime.strptime(date, "%Y-%m-%d")

    return pd.Index(
        list(chain(
            pd.DatetimeIndex(freq='1min', start=date.replace(hour=9, minute=31), end=date.replace(hour=11, minute=30)),
            pd.DatetimeIndex(freq='1min', start=date.replace(hour=13, minute=1), end=date.replace(hour=15, minute=0))
        ))
    )


def sz_slice(f):
    if f.index[-1].hour == 15:
        index = f.index.tolist()
        index[-1] = index[-1].replace(minute=0, second=0)
        f.index = index
    return f


def is_sz(code):
    return code.endswith('.XSHE')
