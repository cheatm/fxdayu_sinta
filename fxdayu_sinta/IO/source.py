from tushare import get_k_data
from fxdayu_sinta.IO.sina_tick import history_tick
from fxdayu_sinta.utils.code import fold, tick_code
from datetime import datetime, timedelta
import pandas as pd


FORMAT = "%Y-%m-%d"


def day(code, *args, **kwargs):
    result = get_k_data(fold(code), *args, **kwargs)
    result.pop('code')
    result['status'] = 0
    return result.set_index('date')


def market_index(code, start="", end="", **kwargs):
    result = get_k_data(fold(code), start, end, index=True, **kwargs)
    result.pop("code")
    result['volume'] *= 100
    result.index = pd.to_datetime(result.pop("date")) + timedelta(hours=15)
    return result


def history(code, date, **kwargs):
    if not isinstance(date, datetime):
        date = datetime.strptime(date, FORMAT)

    tick = history_tick(tick_code(code), date, **kwargs)
    return tick[['price', 'volume', 'amount']]
