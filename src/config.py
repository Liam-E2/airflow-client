import os
import json

SRC_DIR = os.path.dirname(__file__)


def get_config():
    with open(os.path.join(SRC_DIR, 'config.json'), 'rb') as f:
        return json.load(f)
