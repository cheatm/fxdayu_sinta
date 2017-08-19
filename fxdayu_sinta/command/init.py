from fxdayu_sinta.IO.environment import get_env
from fxdayu_sinta.IO.master import Master
from fxdayu_sinta.IO.freq import Freq
from fxdayu_sinta.utils.field import START_OPTION_EMPTY, END_OPTION_EMPTY
import click
import os


class Init(object):

    def __init__(self):
        self.env = get_env()

    def create(self, start="", end="", cover=False):
        self.create_root()
        for code in self.env.stocks:
            self.create_stock(code, start, end, cover)

    def check(self):
        if not os.path.exists(self.env.file_root):
            click.echo('File root dir: %s does not exist' % self.env.file_root)
            return
        else:
            for code in self.env.stocks:
                if Master.env(code).exist:
                    click.echo("%s master OK" % code)
                else:
                    click.echo("%s master missing" % code)

                if Freq.env(code).exist:
                    click.echo("%s freq OK" % code)
                else:
                    click.echo("%s freq missing" % code)

    @staticmethod
    def create_stock(code, start, end, cover):
        master = Master.env(code)
        freq = Freq.env(code)
        if not os.path.exists(master.dir):
            os.makedirs(master.dir)

        if (not master.exist) or cover:
            master.create(start, end)
            master.flush()
            click.echo("Create master %s" % code)

        if (not freq.exist) or cover:
            freq.create()
            freq.flush()
            click.echo("Create freq %s" % code)

    def create_root(self):
        root = self.env.file_root
        if not os.path.exists(root):
            os.makedirs(root)

        log_dir = os.path.join(root, "log")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)



def create_config(root_dir):
    from fxdayu_sinta.IO.config import STORAGE, FILES, CODES, path, root
    from fxdayu_sinta.IO.default import storage
    from fxdayu_sinta.IO.codes import codes
    import json

    if not os.path.exists(root):
        os.makedirs(root)

    storage[FILES] = root_dir
    json.dump(storage, open(path(STORAGE), 'w'))

    json.dump(codes, open(path(CODES), 'w'))

    click.echo("Create config files in %s" % root)


def show():
    from fxdayu_sinta.IO.config import root

    click.echo(root)


def generate():

    init = Init()

    init_group = click.Group(
        "init",
        {"check": click.Command("check", callback=init.check, short_help="Find if required index files exist."),
         "create": click.Command("create", callback=init.create, short_help="Create require index files.",
                                 params=[START_OPTION_EMPTY, END_OPTION_EMPTY,
                                         click.Option(['-c', '--cover'], is_flag=True, flag_value=True, default=False,
                                                      help="If enabled, create file whether target file exists.")]),
         "config": click.Command("config", callback=create_config, short_help="Create config files.",
                                 params=[click.Argument(["root_dir"], nargs=1)]),
         "show": click.Command("show", callback=show, short_help="Show default config files dir.")},
        short_help="Init file system and create index files.",
        chain=True
    )
    return {'init': init_group}