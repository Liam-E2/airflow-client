import os, platform
import json
import subprocess

SRC_DIR = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(SRC_DIR, 'config.json')

def get_config():
    with open(CONFIG_FILE, 'rb') as f:
        return json.load(f)


def edit_config(*args, **kwargs):
    if platform.system() == 'Windows':
        os.startfile(CONFIG_FILE)

    subprocess.check_call(["open", CONFIG_FILE])
