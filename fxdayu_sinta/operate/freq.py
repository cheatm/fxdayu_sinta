from fxdayu_sinta.IO.log import TimeRotateLoggerInterface
from fxdayu_sinta.IO.environment import get_env
from fxdayu_sinta.IO.freq import Freq


class FreqOperate(object):

    def __init__(self, freq, dm):
        self.freq = freq
        self.dm = dm

    @classmethod
    def config(cls, code, freq):
        from fxdayu_sinta.IO.db_manager import DBManager

        return cls(Freq.config(code), DBManager.config())

    def check(self, freq, start=None, end=None):
        freq_col = self.dm[self.freq.code, freq]
        for date in self.freq.find(0, freq, start, end):
            if freq_col.exist(date):
                self.freq[date, freq] = 1
        self.freq.flush()

    def create(self):
        self.freq.create()
        self.freq.flush()

    def update(self):
        self.freq.update()
        self.freq.flush()


class LogFreqOperate(FreqOperate, TimeRotateLoggerInterface):

    NAME = "FreqIndexLog"

    def create(self):
        try:
            super(LogFreqOperate, self).create()
        except Exception as e:
            self.logger.error("%s create freq fail: %s" % (self.freq.code, e))
        else:
            self.logger.info("%s create freq success" % self.freq.code)

    def update(self):
        try:
            super(LogFreqOperate, self).update()
        except Exception as e:
            self.logger.error("%s update freq fail: %s" % (self.freq.code, e))
        else:
            self.logger.info("%s update freq success" % self.freq.code)

    def check(self, freq, start=None, end=None):
        for f in freq.split(','):
            try:
                super(LogFreqOperate, self).check(f, start, end)
            except Exception as e:
                self.logger.error("%s check %s fail: %s" % (self.freq.code, f, e))
            else:
                self.logger.info("%s check %s success" % (self.freq.code, f))

    @classmethod
    def env(cls, code):
        env = get_env()

        return cls(Freq(env.file_root, code, env.freq), env.db_manager)

