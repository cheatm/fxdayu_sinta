import pika


STOP = "StopWorker"


class TornadoWorker(object):

    def __init__(self, worker, parameters):
        self.parameters = parameters
        self.connection = self.connect()
        self.channel = None
        self.worker = worker

    def connect(self):
        return pika.TornadoConnection(
            self.parameters,
            self.on_connection_open,
            on_close_callback=self.on_connection_close
        )

    def on_connection_close(self, connection, reply_code, reply_text):
        if reply_text == STOP:
            self.connection.ioloop.stop()
        else:
            self.connection = self.connect()

    def on_connection_open(self, connection):
        self.channel = connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        self.worker.on_channel_open(channel)

    @classmethod
    def params(cls, worker, *args, **kwargs):
        return cls(worker, pika.ConnectionParameters(*args, **kwargs))

    def start(self):
        self.connection.ioloop.start()


class Worker(object):

    def on_channel_open(self, channel):
        pass


class Consumer(Worker):

    def __init__(self, callback, queue, consume):
        self.channel = None
        self.callback = callback
        self.queue = queue
        self.consume = consume

    def on_channel_open(self, channel):
        self.channel = channel
        self.channel.queue_declare(self.on_queue_open, **self.queue)

    def on_queue_open(self, frame):
        self.channel.basic_consume(self.callback, **self.consume)


class Producer(Worker):

    def __init__(self, iterable, exchange, queue, bind, publish=None):
        self.channel = None
        self.iterable = iterable
        self.exchange = exchange
        self.queue = queue
        bind['queue'] = queue['queue']
        bind['exchange'] = exchange['exchange']
        self.bind = bind
        self.publish = publish if publish else {}

    def on_channel_open(self, channel):
        self.channel = channel
        channel.exchange_declare(self.on_exchange_open, **self.exchange)

    def on_exchange_open(self, frame):
        self.channel.queue_declare(self.on_queue_open, **self.queue)

    def on_queue_open(self, frame):
        self.channel.queue_bind(self.on_bind, **self.bind)

    def on_bind(self, frame):
        exchange = self.bind['exchange']
        routing_key = self.bind['routing_key']
        for message in self.iterable:
            self.channel.basic_publish(
                exchange, routing_key, message,
                **self.publish
            )
        self.channel.connection.close(reply_text=STOP)