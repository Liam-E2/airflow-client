import os, platform, getpass
import json
from dataclasses import dataclass, asdict
import subprocess

SRC_DIR = os.path.join(os.path.expanduser('~'+getpass.getuser()), 'airflow_pycli')
CONFIG_FILE = os.path.join(SRC_DIR, 'config.json')


@dataclass
class ClientConfig:
    airflow_session_token: str = None
    airflow_base_url: str = None
    dag_list_cols: 'list[str]' = None

    def __post_init__(self):
        if self.dag_list_cols is None:
            self.dag_list_cols = ['dag_id', 'description', 'last_parsed_time', 'schedule_interval', 'is_active', 'is_paused', 'has_import_errors', 'tags']


def get_config():
    with open(CONFIG_FILE, 'rb') as f:
        return json.load(f)


def edit_config(*args, **kwargs):
    print(CONFIG_FILE)
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(SRC_DIR, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(asdict(ClientConfig()), f, indent=4)
    
    if platform.system() == 'Windows':
        os.startfile(CONFIG_FILE)
    else:
        subprocess.check_call(["open", CONFIG_FILE])
