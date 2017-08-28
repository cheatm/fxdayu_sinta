import click


def update_bundle():
    import rqalpha
    from fxdayu_sinta.adjust.env import get_home

    rqalpha.update_bundle(get_home(), confirm=False)


def generate():
    return {"update_bundle": click.Command("update_bundle",
                                           callback=update_bundle,
                                           short_help="Update rqalpha bundle data.")}