import click
import importlib
from fxdayu_sinta.IO.environment import init_env

init_env()

command_list = ["fxdayu_sinta.command.master",
                "fxdayu_sinta.command.requester",
                "fxdayu_sinta.command.freq",
                "fxdayu_sinta.command.writer",
                "fxdayu_sinta.command.init",
                "fxdayu_sinta.command.idx"]
commands = {}


for name in command_list:
    module = importlib.import_module(name)
    commands.update(module.generate())


sinta = click.Group('sinta', commands)
