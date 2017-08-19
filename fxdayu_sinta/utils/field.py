class Field(object):

    def __init__(self):
        self.fields = list()

    def set_fields(self, fields):
        self.fields = fields

    def multi(self, item):
        def multi(*args, **kwargs):
            for obj in self:
                getattr(obj, item)(*args, **kwargs)
        return multi

    def __iter__(self):
        for item in self.fields:
            yield self.get(item)

    def get(self, name):
        pass


class CommandField(Field):

    def set_fields(self, fields):
        if fields is None:
            from fxdayu_sinta.IO.config import get_codes, STOCK
            super(CommandField, self).set_fields(get_codes()[STOCK])
        else:
            super(CommandField, self).set_fields(fields.split(','))


from click import Option, STRING

FIELD_OPTION = Option(['-f', '--fields'], type=STRING, default=None, required=False,
                      help="Specify fields of stock like 000001.XSHE,000002.XSHE .")
START_OPTION = Option(["-s", "--start"], type=STRING, default=None, required=False,
                      help="Time format: yyyy-mm-dd")
END_OPTION = Option(["-e", "--end"], type=STRING, default=None, required=False,
                    help="Time format: yyyy-mm-dd")
END_OPTION_EMPTY = Option(["-e", "--end"], type=STRING, default="", required=False,
                          help="Time format: yyyy-mm-dd")
START_OPTION_EMPTY = Option(["-s", "--start"], type=STRING, default="", required=False,
                            help="Time format: yyyy-mm-dd")
FREQ_OPTION = Option(['--freq'], type=STRING, default=None, required=False,
                     help="Specify frequency like H,D .")
