from fxdayu_sinta.operate.writer import Writer
from fxdayu_sinta.IO.master import Master
from fxdayu_sinta.IO.freq import Freq
from fxdayu_sinta.IO.environment import get_env


class WriteField(object):

    def __init__(self):
        self.field = list()
        self.writer = Writer()
        self.env = get_env()

    def set_fields(self, fields):
        if fields is None:
            self.field = self.env.stocks
        else:
            self.field = fields.split(",")

    def iter_main(self):
        for code in self.field:
            yield Master.env(code), self.env.db_manager[code]

    def iter_freq(self, freq):
        for code in self.field:
            yield Freq.env(code), self.env.db_manager[code, freq], Master.env(code), self.env.db_manager[code]

    def master(self, start=None, end=None):
        for params in self.iter_main():
            self.writer.master(*params, start=start, end=end)

    def freq(self, freq=None, start=None, end=None):
        if freq is None:
            freq = self.env.freq
        else:
            freq = freq.split(',')

        for f in freq:
            for params in self.iter_freq(f):
                self.writer.freq(*params, start=start, end=end)


def generate():
    import click
    from fxdayu_sinta.utils.field import START_OPTION, END_OPTION, FREQ_OPTION, FIELD_OPTION

    writer = WriteField()

    write = click.Group(
        "write",
        {"master": click.Command("master", callback=writer.master,
                                 params=[START_OPTION, END_OPTION],
                                 short_help="Read tick and write 1min into db."),
         "freq": click.Command("freq", callback=writer.freq,
                               params=[FREQ_OPTION, START_OPTION, END_OPTION],
                               short_help="Read 1min write other frequency into db.")},
        callback=writer.set_fields,
        params=[FIELD_OPTION],
        short_help="Write data into db by index."
    )
    return {"write": write}


