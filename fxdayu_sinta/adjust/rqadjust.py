import importlib
import click

command_list = ["fxdayu_sinta.adjust.env",
                "fxdayu_sinta.adjust.writer",
                "fxdayu_sinta.adjust.bundle"]

commands = {}


for name in command_list:
    module = importlib.import_module(name)
    commands.update(module.generate())


rqadjust = click.Group("rqadjust", commands)


if __name__ == '__main__':
    import sys
    sys.argv.append("update")
    rqadjust()
