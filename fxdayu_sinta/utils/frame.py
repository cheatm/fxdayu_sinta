import pandas as pd
from datetime import datetime
from itertools import chain
from fxdayu_sinta.IO.sina_tick import tick2min
from fxdayu_data.tools.resampler import Resampler


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
