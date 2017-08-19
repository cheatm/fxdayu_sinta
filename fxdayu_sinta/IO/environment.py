from fxdayu_sinta.IO import config, ENV_TAG


class Environment(object):

    def __init__(self):
        self.storage = config.get_storage()
        self.dm = None

    @property
    def file_root(self):
        return self.storage[config.FILES]

    @property
    def freq(self):
        return self.storage[config.FREQ]

    @property
    def mongo(self):
        return self.storage[config.MONGO]

    @property
    def stocks(self):
        return config.get_codes()[config.STOCK]

    @property
    def market_index(self):
        return config.get_codes()[config.MARKETINDEX]

    @property
    def db_manager(self):
        if self.dm is not None:
            return self.dm
        else:
            from fxdayu_sinta.IO.db_manager import DBManager, create_client
            from fxdayu_sinta.IO import MONGO

            mongo = self.storage[MONGO]
            self.dm = DBManager(create_client(mongo['client']), mongo['main'], mongo['freq'])
            return self.dm


def init_env():
    globals()[ENV_TAG] = Environment()


def get_env():
    return globals()[ENV_TAG]
