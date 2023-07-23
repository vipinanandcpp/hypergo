import datetime
import os
from typing import List
import yaml
from colors import color

from hypergo.config import Config
from hypergo.graph import graph as hypergraph
from hypergo.version import get_version
from hypergo.stdio_connection import StdioConnection
from hypergo.local_storage import LocalStorage

import sys

def format_date(sec: float) -> str:
    dtf: str = '%b %d %Y, %H:%M:%S.%f'
    return datetime.datetime.fromtimestamp(sec).strftime(dtf)[:-3]

def get_version_path() -> str:
    return os.path.dirname(os.path.abspath(__file__)) + '/version.py'

def load_config(*config_paths: str) -> Config:
    unmerged_data: List[dict] = []
    paths = list(config_paths)
    for path in paths:
        with open(path, "r") as fh:
            file_data = yaml.safe_load(fh)
        unmerged_data.append(file_data)
    return unmerged_data[0]


class HypergoCli:
    @property
    def prompt(self) -> str:
        return f'{color("hypergo", fg="#33ff33")} {color("∵", fg="#33ff33")} '

    @property
    def intro(self) -> str:
        version: str = get_version()
        timestamp: str = format_date(os.path.getmtime(get_version_path()))
        intro: str = f'hypergo {version} ({timestamp})\nType help or ? to list commands.'
        return str(color(intro, fg='#ffffff'))

    def run(self, ref: str, *args: str) -> int:
        try:
            config: Config = load_config(ref, *args)
            if not sys.stdin.isatty():
                stdin_data = sys.stdin.read().strip()
                if stdin_data:
                    args = (stdin_data,) + args

            connection = StdioConnection()
            result = connection.consume(args[0], config, LocalStorage().use_sub_path("private_storage"))

        except Exception as err:
            print(f'*** {err}')
            raise err
        return 0

    def use(self, name: str) -> int:
        return 0

    def init(self, name: str) -> int:
        try:
            os.makedirs(f'.hypergo/{name}')
        except FileExistsError:
            pass
        self.use(name)
        return 0

    def start(self, ref: str, *args: str) -> int:
        config = load_config(ref, *args)
        raise ValueError(f'unexpected protocol: {config.protocol}')

    def graph(self, *args: str) -> int:
        hypergraph(list(args))
        return 0
