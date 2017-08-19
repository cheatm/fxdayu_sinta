from fxdayu_sinta.IO.log import TimeRotateLoggerInterface
from fxdayu_sinta.IO.source import market_index
from fxdayu_data.handler.mongo_handler import update
from fxdayu_sinta.IO.environment import get_env, init_env
from fxdayu_sinta.IO import MONGO, FREQ


class IdxRequester(TimeRotateLoggerInterface):

    NAME = "MarketIndexLog"

    def __init__(self, db):
        self.fields = list()
        self.db = db

    def set_fields(self, fields):
        if fields is not None:
            self.fields = fields.split(",")
        else:
            self.fields = get_env().market_index

    def save(self, code, start='', end=''):
        try:
            data = market_index(code, start, end)
            update(self.db[code], data)
        except Exception as e:
            self.logger.error("save %s fail: %s" % (code, e))
        else:
            self.logger.info("save %s success" % code)

    def request(self, fields=None, start="", end=""):
        self.set_fields(fields)
        for code in self.fields:
            self.save(code, start, end)

    @classmethod
    def env(cls):
        env = get_env()
        db = env.mongo[FREQ]["D"]["db"]
        return cls(env.db_manager.client[db])
