

def handle_exception(e, function, *args, **kwargs):
    print "{} {} {}".format(function, args, kwargs)
    print e


def retry(count=3, exception=Exception, handle=handle_exception, default=lambda *args, **kwargs: None, wait=1):
    def wrapper(function):
        from time import sleep

        def re(*args, **kwargs):
            for i in range(count):
                try:
                    return function(*args, **kwargs)
                except exception as e:
                    handle(e, function, *args, **kwargs)
                    sleep(wait)
            return default(*args, **kwargs)
        return re
    return wrapper