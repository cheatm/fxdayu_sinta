from fxdayu_sinta.utils.field import CommandField, \
    FIELD_OPTION, START_OPTION, END_OPTION, START_OPTION_EMPTY, END_OPTION_EMPTY
from fxdayu_sinta.operate.master import LogMasterOperate


class MasterField(CommandField):

    def get(self, name):
        return LogMasterOperate.env(name)


def generate():
    import click

    master = MasterField()
    return {
        "master": click.Group(
            "master",
            commands={
                "create": click.Command(name="create", callback=master.multi("create"),
                                        params=[START_OPTION_EMPTY, END_OPTION_EMPTY],
                                        short_help="Create master index."),
                "update": click.Command(name="update", callback=master.multi("update"),
                                        params=[START_OPTION_EMPTY, END_OPTION_EMPTY],
                                        short_help="Update master index."),
                "file": click.Command(name="file", callback=master.multi("file"),
                                      params=[START_OPTION, END_OPTION],
                                      short_help="Check tick data in file and modify master index."),
                "db": click.Command(name="db", callback=master.multi("db"),
                                    params=[START_OPTION, END_OPTION],
                                    short_help="Check data in db and modify master index.")
            },
            callback=master.set_fields,
            params=[FIELD_OPTION],
            short_help="Modify master index."
        )
    }