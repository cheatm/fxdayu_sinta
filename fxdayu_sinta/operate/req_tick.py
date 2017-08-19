from fxdayu_sinta.IO.log import TimeRotateLoggerInterface
from threading import Thread
from fxdayu_sinta.utils import retry
from fxdayu_sinta.IO.sina_tick import SinaBreak
from fxdayu_sinta.IO.source import history
from fxdayu_sinta.IO.config import get_files, get_codes, STOCK
from time import sleep
from fxdayu_sinta.IO.master import Master
import json


def fail(master, date, **kwargs):
    return master.code, date, 0


class TickRequester(Thread, TimeRotateLoggerInterface):

    NAME = "TickRequestLog"

    def __init__(self):
        super(TickRequester, self).__init__()
        self.root = get_files()
        self.save_tick = retry(handle=self.handle, default=fail, count=2)(self.save_tick)
        self._running = False

    def start(self):
        if not self._running and not self.isAlive():
            self._running = True
            super(TickRequester, self).start()

    def stop(self):
        if self._running:
            self._running = False
            self.join()

    def run(self):
        while self._running:
            self.logger.info("listening tick")
            sleep(120)

    def handle(self, e, func, master, date, **kwargs):
        if isinstance(e, SinaBreak):
            self.logger.error("save tick %s %s fail: SinaBreak Wait for 2 minutes" % (master.code, date))
            sleep(120)
        else:
            self.logger.error("save tick %s %s fail: %s" % (master.code, date, e))

    def save_tick(self, master, date, **kwargs):
        code = master.code
        tick = history(code, date, **kwargs)
        master.write(date, tick)
        return code, date, 1

    def save_stock(self, code, start, end):
        master = Master(self.root, code)
        for date in master.find(0, start, end):
            result = self.save_tick(master, date)
            self.logger.info("tick %s %s %s" % result)
            sleep(1)

    def request(self, fields=None, start=None, end=None, routing=True):
        if routing:
            self.start()
        if fields is None:
            fields = get_codes()[STOCK]
        else:
            fields = fields.split(",")
        for code in fields:
            self.save_stock(code, start, end)
        self.stop()


