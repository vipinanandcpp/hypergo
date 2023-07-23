import cmd
from typing import IO, List, Optional, cast
from hypergo.hypergo_cli import HypergoCli
import sys

class HypergoCmd(cmd.Cmd):
    intro: str = ''
    prompt: str = ''

    def __init__(self, cli: HypergoCli, completekey: str = 'tab', stdin: Optional[IO[str]] = None, stdout: Optional[IO[str]] = None) -> None:
        super().__init__(completekey, stdin, stdout)
        self._cli = cli
        HypergoCmd.intro = self._cli.intro
        HypergoCmd.prompt = self._cli.prompt

    def onecmd(self, line: str) -> bool:
        splitline: List[str] = line.split()
        command: str = splitline[0]
        if hasattr(self, f'do_{command}') or not hasattr(self._cli, command):
            return super().onecmd(line)

        args: List[str] = splitline[1:]
        return cast(callable, getattr(self._cli, command))(args[0], *args[1:])

    def do_exit(self, line: str) -> bool:
        return True
