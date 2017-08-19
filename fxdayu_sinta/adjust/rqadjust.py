import importlib
import click

command_list = ["fxdayu_sinta.adjust.env",
                "fxdayu_sinta.adjust.writer"]

import sys
sys.path.insert(0, "D:\\fxdayu_sinta")

commands = {}


for name in command_list:
    module = importlib.import_module(name)
    commands.update(module.generate())


rqadjust = click.Group("rqadjust", commands)


if __name__ == '__main__':
    rqadjust()
