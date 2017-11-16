import click
from fxdayu_sinta.operate.req_tick import TickRequester
from fxdayu_sinta.utils.field import START_OPTION, END_OPTION, FIELD_OPTION


def generate():

    tick = TickRequester()
    command = click.Command(name='tick', callback=tick.request,
                            params=[FIELD_OPTION, START_OPTION, END_OPTION,
                                    click.Option(['--routing/--no-routing'], default=True)],
                            short_help="Request tick data and save into .xlsx file.")

    return {
        "request": click.Group(
            "request",
            {"tick": command},
            short_help="Initialize config and file system."
        )
    }