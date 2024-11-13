import os, platform, getpass
import json
from dataclasses import dataclass
import subprocess

SRC_DIR = os.path.join(os.path.expanduser('~'+getpass.getuser()), 'airflow_pycli')
CONFIG_FILE = os.path.join(SRC_DIR, 'config.json')


@dataclass
class ClientConfig:
    airflow_session_token: str
    airflow_base_url: str


def get_config():
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(SRC_DIR, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump({}, f)

    with open(CONFIG_FILE, 'rb') as f:
        return json.load(f)


def edit_config(*args, **kwargs):
    if platform.system() == 'Windows':
        os.startfile(CONFIG_FILE)

    subprocess.check_call(["open", CONFIG_FILE])
