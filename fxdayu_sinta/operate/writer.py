from fxdayu_sinta.utils.frame import candle, Resampler
from fxdayu_sinta.IO.log import TimeRotateLoggerInterface

resample = Resampler().resample


def write_master(master, master_db, date):
    data = candle(master.code, date, master.read(date))
    master_db.write(data)


def write_freq(freq_db, master_db, date):
    data = resample(master_db[date], freq_db.freq)
    freq_db.write(data)


class Writer(TimeRotateLoggerInterface):
    NAME = "WriteLog"

    def master(self, master, master_db, start=None, end=None):
        for date in master.find(1, start, end):
            self.write_master(master, master_db, date)

    def write_master(self, master, master_db, date):
        try:
            write_master(master, master_db, date)
        except Exception as e:
            self.logger.error("master %s %s fail: %s" % (master.code, date, e))
        else:
            self.logger.info("master %s %s success" % (master.code, date))

    def freq(self, freq_file, freq_db, master_file, master_db, start=None, end=None):
        for date in freq_file.find(0, freq_db.freq, start, end):
            if master_file[date] == 2:
                self.write_freq(master_file.code, freq_db, master_db, date)

    def write_freq(self, code, freq_db, master_db, date):
        try:
            write_freq(freq_db, master_db, date)
        except Exception as e:
            self.logger.error("%s %s %s fail: %s" % (freq_db.freq, code, date, e))
        else:
            self.logger.info("%s %s %s success" % (freq_db.freq, code, date))