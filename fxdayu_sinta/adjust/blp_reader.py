import pandas as pd
import bcolz
import six
from collections import Iterable
from datetime import datetime


class BLPTable(object):

    def __init__(self, rootdir, index):
        self.table = bcolz.ctable(rootdir=rootdir, mode='r')
        self.line_map = self.table.attrs.attrs['line_map']
        self.index = self.table.cols[index]

    def read(self, names, start=None, end=None, length=None, columns=None):
        if columns is None:
            columns = self.table.names
        if isinstance(columns, six.string_types):
            columns = (columns,)

        if isinstance(names, six.string_types):
            return self._read(names, start, end, length, columns)
        elif isinstance(names, Iterable):
            return pd.Panel.from_dict(
                {name: self._read(name, start, end, length, columns) for name in names}
            )

    def _read(self, name, start, end, length, columns):
        index_slice = self._index_slice(name, start, end, length)

        return pd.DataFrame(
            {key: self._read_line(index_slice, key) for key in columns},
            index=self._read_index(index_slice)
        )

    def _read_line(self, index, column):
        return self.table.cols[column][index]

    def _read_index(self, index):
        return self.index[index]

    def _index_slice(self, name, start, end, length):
        head, tail = self.line_map[name]
        index = self.index[head:tail]
        if start:
            s = index.searchsorted(start)
            if end:
                e = index.searchsorted(end, 'right')
                return slice(head+s, head+e)
            elif length:
                return slice(head+s, head+s+length)
            else:
                return slice(head+s, tail)
        elif end:
            e = index.searchsorted(end, 'right')
            if length:
                return slice(head+e-length, head+e)
            else:
                return slice(head, head+e)
        elif length:
            return slice(tail-length, tail)
        else:
            return slice(head, tail)


def num2date(num):
    return datetime.strptime(str(num), "%Y%m%d000000")


def transfer(frame):
    return pd.DataFrame({'adjust': frame['ex_cum_factor'].values}, list(map(num2date, frame.index)))


class ExFactor(BLPTable):

    @classmethod
    def conf(cls):
        from fxdayu_sinta.adjust.env import get_adj_dir
        return cls(get_adj_dir(), "start_date")

    def _read(self, name, start, end, length, columns):
        try:
            return transfer(super(ExFactor, self)._read(name, start, end, length, columns))
        except Exception:
            return super(ExFactor, self)._read(name, start, end, length, columns)

if __name__ == '__main__':
    reader = ExFactor("E:\\rqalpha\\bundle\\ex_cum_factor.bcolz", 'start_date')