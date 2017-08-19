import os
import pandas as pd
from fxdayu_sinta.IO.source import day
from fxdayu_sinta.utils.frame import expand


STATUS = "status"


class Master(object):
    def __init__(self, root, code):
        self.root = root
        self.code = code
        self.dir = os.path.join(root, code)
        self.path = os.path.join(self.dir, 'index.csv')

        if os.path.exists(self.path):
            self.table = pd.read_csv(self.path, index_col='date')
        else:
            self.table = pd.DataFrame()

    @property
    def exist(self):
        return os.path.exists(self.path)

    def create(self, start='', end=''):
        self.table = day(self.code, start, end)

    def update(self, start='', end=''):
        new = day(self.code, start, end)
        self.table = expand(self.table, new)

    def locate(self, start, end):
        if start:
            index = self.table.index >= start

        if end:
            index = self.table.index <= end

        if "index" in locals():
            return self.table[index]
        else:
            return self.table

    def find(self, value, start=None, end=None):
        table = self.locate(start, end)
        return table.index[table['status'] == value]

    def find_not(self, value, start=None, end=None):
        table = self.locate(start, end)
        return table.index[table['status'] != value]

    def __getitem__(self, item):
        return self.table.loc[item, STATUS]

    def __setitem__(self, key, value):
        self.table.loc[key, STATUS] = value

    def flush(self):
        self.table.to_csv(self.path)

    def write(self, date, frame):
        frame.to_excel(self.tick_path(date))

    def read(self, date):
        return pd.read_excel(self.tick_path(date))

    def tick_exist(self, date):
        return os.path.exists(self.tick_path(date))

    def tick_path(self, date):
        return os.path.join(self.dir, date+'.xlsx')

    @classmethod
    def config(cls, code):
        from fxdayu_sinta.IO.config import get_files

        return cls(get_files(), code)

    @classmethod
    def env(cls, code):
        from fxdayu_sinta.IO.environment import get_env

        return cls(get_env().file_root, code)
