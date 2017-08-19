from fxdayu_sinta.utils.mongo import update
from fxdayu_sinta.IO.log import TimeRotateLoggerInterface
from fxdayu_sinta.adjust.blp_reader import ExFactor
import six


class AdjustWriter(object):

    def __init__(self, reader, db):
        self.reader = reader
        self.db = db

    @classmethod
    def env(cls):
        from fxdayu_sinta.adjust.env import get_db

        return cls(ExFactor.conf(), get_db())

    def write(self, code):
        adjust = self.reader.read(code)
        update(self.db[code], adjust, index='start')

    def update(self, code):
        adjust = self.reader.read(code)
        doc = self.db[code].find_one(sort=[("start", -1)])

        if ("start" not in doc) or (adjust.index[-1] > doc["start"]):
            update(self.db[code], adjust, index='start')

    def __call__(self, fields=None):
        if fields is None:
            from fxdayu_sinta.IO.config import get_codes, STOCK
            fields = get_codes()[STOCK]
        elif isinstance(fields, six.string_types):
            fields = fields.split(",")

        for code in fields:
            self.write(code)


class LogAdjustWriter(AdjustWriter, TimeRotateLoggerInterface):
    NAME = "AdjustLog"

    def fields(self, fields):
        if fields is None:
            from fxdayu_sinta.IO.config import get_codes, STOCK
            return get_codes()[STOCK]
        elif isinstance(fields, six.string_types):
            return fields.split(",")
        else:
            return fields

    def write(self, code):
        try:
            super(LogAdjustWriter, self).write(code)
        except Exception as e:
            self.logger.error("save adjust %s fail: %s" % (code, e))
        else:
            self.logger.info("save adjust %s success" % code)

    def update(self, code):
        try:
            super(LogAdjustWriter, self).update(code)
        except Exception as e:
            self.logger.error("update adjust %s fail: %s" % (code, e))
        else:
            self.logger.info("update adjust %s success" % code)

    def writes(self, fields):
        for code in self.fields(fields):
            self.write(code)

    def updates(self, fields):
        for code in self.fields(fields):
            self.update(code)


def generate():
    import click
    from fxdayu_sinta.utils.field import FIELD_OPTION

    law = LogAdjustWriter.env()

    return {'write': click.Command("write", callback=law.writes, params=[FIELD_OPTION],
                                   short_help="Read rqalpha adjust factor and write into mongodb"),
            'update': click.Command("update", callback=law.updates, params=[FIELD_OPTION],
                                    short_help="Read rqalpha adjust factor and write into mongodb if rqalpha updated")}
