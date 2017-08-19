import os
import pandas as pd
from fxdayu_sinta.IO.environment import get_env


class Freq(object):

    def __init__(self, root, code, frequency):
        self.root = root
        self.code = code
        self.path = os.path.join(root, code, 'freq.csv')
        self.freq = frequency

        if os.path.exists(self.path):
            self.table = pd.read_csv(self.path, index_col='date')
        else:
            self.table = pd.DataFrame(columns=self.freq)

    @property
    def exist(self):
        return os.path.exists(self.path)

    def create(self):
        master = os.path.join(self.root, self.code, 'index.csv')
        if os.path.exists(master):
            master = pd.read_csv(master, index_col='date')
            self.table = pd.DataFrame(0, master.index, self.freq)
        else:
            raise IOError("Master: %s does not exist" % master)

    def update(self):
        master = os.path.join(self.root, self.code, 'index.csv')
        if os.path.exists(master):
            master = pd.read_csv(master, index_col='date')
            self.table = pd.DataFrame(self.table, master.index).fillna(0)
        else:
            raise IOError("Master: %s does not exist" % master)

    def find(self, value, freq, start=None, end=None):
        table = self.locate(start, end)
        return table.index[table[freq] == value]

    def find_not(self, value, freq, start=None, end=None):
        table = self.locate(start, end)
        return table.index[table[freq] == value]

    def locate(self, start, end):
        if start:
            index = self.table.index >= start

        if end:
            index = self.table.index <= end

        if "index" in locals():
            return self.table[index]
        else:
            return self.table

    def __getitem__(self, item):
        return self.table.loc[item]

    def __setitem__(self, key, value):
        self.table.loc[key] = value

    def flush(self):
        self.table.to_csv(self.path)

    @classmethod
    def config(cls, code):
        from fxdayu_sinta.IO.config import get_storage, FILES, FREQ

        storage = get_storage()
        return cls(storage[FILES], code, storage[FREQ])

    @classmethod
    def env(cls, code):
        env = get_env()

        return cls(env.file_root, code, env.freq)
