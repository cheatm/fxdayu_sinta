from fxdayu_sinta.IO.log import TimeRotateLoggerInterface
from fxdayu_sinta.IO.environment import get_env
from fxdayu_sinta.IO.master import Master


class MasterOperate(object):

    def __init__(self, master, stock_db):
        self.master = master
        self.stock_db = stock_db

    @classmethod
    def config(cls, code):
        from fxdayu_sinta.IO.master import Master
        from fxdayu_sinta.IO.db_manager import DBManager

        return cls(Master.config(code),
                   DBManager.config()[code])

    @classmethod
    def env(cls, code):
        from fxdayu_sinta.IO import ENV_TAG
        from fxdayu_sinta.IO.master import Master

        env = globals()[ENV_TAG]
        return cls(
            Master(env.file_root, code),
            env.db_manager[code]
        )

    def file(self, start=None, end=None):
        for date in self.master.find(0, start, end):
            if self.master.tick_exist(date):
                self.master[date] = 1
        self.master.flush()

    def db(self, start=None, end=None):
        for date in self.master.find_not(2, start, end):
            if self.stock_db.exist(date):
                self.master[date] = 2
        self.master.flush()

    def create(self, start="", end=""):
        self.master.create(start, end)
        self.master.flush()

    def update(self, start="", end=""):
        self.master.update(start, end)
        self.master.flush()


class LogMasterOperate(MasterOperate, TimeRotateLoggerInterface):
    NAME = "MainIndexLog"

    def file(self, start=None, end=None):
        try:
            super(LogMasterOperate, self).file(start, end)
        except Exception as e:
            self.logger.error("%s check file fail: %s" % (self.master.code, e))
        else:
            self.logger.info("%s check file success" % self.master.code)

    def db(self, start=None, end=None):
        try:
            super(LogMasterOperate, self).db(start, end)
        except Exception as e:
            self.logger.error("%s check db fail: %s" % (self.master.code, e))
        else:
            self.logger.info("%s check db success" % self.master.code)

    def create(self, start="", end=""):
        try:
            super(LogMasterOperate, self).create(start, end)
        except Exception as e:
            self.logger.error("%s create %s-%s fail: %s" % (self.master.code, start, end, e))
        else:
            self.logger.info("%s create %s-%s success" % (self.master.code, start, end))

    def update(self, start="", end=""):
        try:
            super(LogMasterOperate, self).update(start, end)
        except Exception as e:
            self.logger.error("%s update %s-%s fail: %s" % (self.master.code, start, end, e))
        else:
            self.logger.info("%s update %s-%s success" % (self.master.code, start, end))

    @classmethod
    def env(cls, code):
        env = get_env()
        return cls(
            Master(env.file_root, code),
            env.db_manager[code]
        )