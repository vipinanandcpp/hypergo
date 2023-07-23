import click
from click_default_group import DefaultGroup

from hypergo.hypergo_cli import HypergoCli
from hypergo.hypergo_cmd import HypergoCmd
from typing import Tuple

HYPERGO_CLI = HypergoCli()

@click.group(cls=DefaultGroup, default='shell', default_if_no_args=True)
def main() -> int:
    pass

@main.command()
def shell() -> int:
    HypergoCmd(HYPERGO_CLI).cmdloop()
    return 0

@main.command()
@click.argument('ref', type=click.STRING)
@click.argument('arg', nargs=-1)
@click.option('--stdin', is_flag=True, default=False, help='Read input from stdin.')
def stdio(ref: str, arg: Tuple[str], stdin: bool) -> int:
    arg = (stdin_data,) + arg if stdin and not sys.stdin.isatty() and (stdin_data := sys.stdin.read().strip()) else arg
    return HYPERGO_CLI.stdio(ref, *list(arg))

@main.command()
@click.argument('ref', type=click.STRING)
@click.argument('arg', nargs=-1)
def graph(ref: str, arg: Tuple[str]) -> int:
    return HYPERGO_CLI.graph(ref, *list(arg))
