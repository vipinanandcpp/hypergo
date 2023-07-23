diff --git a/hypergo/hypergo_cli.py b/hypergo/hypergo_cli.py
index 42d984d..9d205e7 100644
--- a/hypergo/hypergo_cli.py
+++ b/hypergo/hypergo_cli.py
@@ -1,9 +1,8 @@
 import datetime
 import os
 from typing import List
-import yaml
 from colors import color
-
+import json
 from hypergo.config import Config
 from hypergo.graph import graph as hypergraph
 from hypergo.version import get_version
@@ -12,23 +11,6 @@ from hypergo.local_storage import LocalStorage
 
 import sys
 
-def format_date(sec: float) -> str:
-    dtf: str = '%b %d %Y, %H:%M:%S.%f'
-    return datetime.datetime.fromtimestamp(sec).strftime(dtf)[:-3]
-
-def get_version_path() -> str:
-    return os.path.dirname(os.path.abspath(__file__)) + '/version.py'
-
-def load_config(*config_paths: str) -> Config:
-    unmerged_data: List[dict] = []
-    paths = list(config_paths)
-    for path in paths:
-        with open(path, "r") as fh:
-            file_data = yaml.safe_load(fh)
-        unmerged_data.append(file_data)
-    return unmerged_data[0]
-
-
 class HypergoCli:
     @property
     def prompt(self) -> str:
@@ -36,18 +18,27 @@ class HypergoCli:
 
     @property
     def intro(self) -> str:
+        def format_date(sec: float) -> str:
+            return datetime.datetime.fromtimestamp(sec).strftime('%b %d %Y, %H:%M:%S.%f')[:-3]
+
+        def get_version_path() -> str:
+            return os.path.dirname(os.path.abspath(__file__)) + '/version.py'
+
         version: str = get_version()
         timestamp: str = format_date(os.path.getmtime(get_version_path()))
         intro: str = f'hypergo {version} ({timestamp})\nType help or ? to list commands.'
         return str(color(intro, fg='#ffffff'))
 
-    def run(self, ref: str, *args: str) -> int:
+    def stdio(self, ref: str, *args: str) -> int:
         try:
-            config: Config = load_config(ref, *args)
+            config: Config = json.load(open(ref, "r"))
+
             if not sys.stdin.isatty():
                 stdin_data = sys.stdin.read().strip()
                 if stdin_data:
                     args = (stdin_data,) + args
+            else:
+                raise BrokenPipeError("No input message piped in through stdin")
 
             connection = StdioConnection()
             result = connection.consume(args[0], config, LocalStorage().use_sub_path("private_storage"))
@@ -55,22 +46,9 @@ class HypergoCli:
         except Exception as err:
             print(f'*** {err}')
             raise err
-        return 0
 
-    def use(self, name: str) -> int:
-        return 0
-
-    def init(self, name: str) -> int:
-        try:
-            os.makedirs(f'.hypergo/{name}')
-        except FileExistsError:
-            pass
-        self.use(name)
         return 0
 
-    def start(self, ref: str, *args: str) -> int:
-        config = load_config(ref, *args)
-        raise ValueError(f'unexpected protocol: {config.protocol}')
 
     def graph(self, *args: str) -> int:
         hypergraph(list(args))
diff --git a/hypergo/hypergo_click.py b/hypergo/hypergo_click.py
index cb1ba6e..1fe65b4 100644
--- a/hypergo/hypergo_click.py
+++ b/hypergo/hypergo_click.py
@@ -20,25 +20,9 @@ def shell() -> int:
 @click.argument('ref', type=click.STRING)
 @click.argument('arg', nargs=-1)
 @click.option('--stdin', is_flag=True, default=False, help='Read input from stdin.')
-def run(ref: str, arg: Tuple[str], stdin: bool) -> int:
+def stdio(ref: str, arg: Tuple[str], stdin: bool) -> int:
     arg = (stdin_data,) + arg if stdin and not sys.stdin.isatty() and (stdin_data := sys.stdin.read().strip()) else arg
-    return HYPERGO_CLI.run(ref, *list(arg))
-
-@main.command()
-@click.argument('name', type=click.STRING)
-def init(name: str) -> int:
-    return HYPERGO_CLI.init(name)
-
-@main.command()
-@click.argument('name', type=click.STRING)
-def use(name: str) -> int:
-    return HYPERGO_CLI.use(name)
-
-@main.command()
-@click.argument('ref', type=click.STRING)
-@click.argument('arg', nargs=-1)
-def start(ref: str, arg: Tuple[str]) -> int:
-    return HYPERGO_CLI.start(ref, *list(arg))
+    return HYPERGO_CLI.stdio(ref, *list(arg))
 
 @main.command()
 @click.argument('ref', type=click.STRING)
diff --git a/hypergo/hypergo_cmd.py b/hypergo/hypergo_cmd.py
index c87b9ba..0065fae 100644
--- a/hypergo/hypergo_cmd.py
+++ b/hypergo/hypergo_cmd.py
@@ -1,6 +1,7 @@
 import cmd
 from typing import IO, List, Optional, cast
 from hypergo.hypergo_cli import HypergoCli
+import sys
 
 class HypergoCmd(cmd.Cmd):
     intro: str = ''
@@ -19,11 +20,6 @@ class HypergoCmd(cmd.Cmd):
             return super().onecmd(line)
 
         args: List[str] = splitline[1:]
-        if not sys.stdin.isatty():
-            stdin_data = sys.stdin.read().strip()
-            if stdin_data:
-                args = [stdin_data] + args
-
         return cast(callable, getattr(self._cli, command))(args[0], *args[1:])
 
     def do_exit(self, line: str) -> bool:
