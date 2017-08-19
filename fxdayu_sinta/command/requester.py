import click
from fxdayu_sinta.operate.req_tick import TickRequester
from fxdayu_sinta.utils.field import START_OPTION, END_OPTION, FIELD_OPTION
from fxdayu_sinta.operate.market_index import IdxRequester


def generate():

    tick = TickRequester()
    idx = IdxRequester.env()
    command = click.Command(name='tick', callback=tick.request,
                            params=[FIELD_OPTION, START_OPTION, END_OPTION,
                                    click.Option(['--routing/--no-routing'], default=True)],
                            short_help="Request tick data and save into .xlsx file.")
    idx_command = click.Command(name="idx", callback=idx.request,
                                params=[FIELD_OPTION, START_OPTION, END_OPTION],
                                short_help="Request market index and save into db")

    return {
        "request": click.Group(
            "request",
            {"tick": command,
             "idx": idx_command},
            short_help="Initialize config and file system."
        )
    }