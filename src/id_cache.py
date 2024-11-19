import json
import os

from .config import SRC_DIR
from traceback import format_exc

ID_CACHE_PATH = os.path.join(SRC_DIR, 'cache.json')


def load_cache():
    if not os.path.exists(ID_CACHE_PATH):
        with open(ID_CACHE_PATH, 'w') as f:
            json.dump({"egads": "no cached ids!"}, f)
    try:
        with open(ID_CACHE_PATH, 'rb') as f:
            data = json.load(f)
            print(data)
        return data
    except Exception as e:
        print(format_exc())


def update_cache(key, value):
    cache_data = load_cache()
    cache_data[key] = value
    with open(ID_CACHE_PATH, 'w') as f:
        json.dump(cache_data, f)
