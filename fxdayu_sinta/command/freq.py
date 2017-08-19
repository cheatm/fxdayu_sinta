from fxdayu_sinta.utils.field import CommandField
from fxdayu_sinta.operate.freq import LogFreqOperate
from fxdayu_sinta.IO.environment import get_env


class FreqField(CommandField):

    def get(self, name):
        return LogFreqOperate.env(name)

    def check(self, freq, start=None, end=None):
        if freq is None:
            freq = get_env().freq
        else:
            freq = freq.split(',')

        for f in freq:
            self.multi('check')(f, start, end)


def generate():
    import click
    from fxdayu_sinta.utils.field import START_OPTION, END_OPTION, FIELD_OPTION

    field = FreqField()

    return {"freq": click.Group(
        "freq",
        {"create": click.Command("create", callback=field.multi("create"), short_help="Create freq index."),
         "update": click.Command("update", callback=field.multi("update"), short_help="Update freq index."),
         "check": click.Command("check", callback=field.check, short_help="Check data in db and modify freq index.",
                                params=[click.Option(['-f', '--freq'], default=None, required=False),
                                        START_OPTION, END_OPTION])},
        callback=field.set_fields,
        params=[FIELD_OPTION],
        short_help="Modify freq index."
    )}




