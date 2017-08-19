
MONGO = "mongo_config"
FILES = "dir_root"
CODES = "codes.json"
STORAGE = "storage.json"
STOCK = "Stock"
MARKETINDEX = "MarketIndex"
LOG = "log"
FREQ = "freq"
ENV_TAG = "global_environment"


def get_env():
    return globals().get(ENV_TAG, None)


