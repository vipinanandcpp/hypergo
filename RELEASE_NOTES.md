# Release Notes

## Version 1.1.0

### HypergoCli Class Updates:
- Added the `stdio` method to the `HypergoCli` class to handle standard input/output.
- Removed the `format_date`, `get_version_path`, `load_config`, `use`, and `start` methods from the `HypergoCli` class.

### HypergoCmd Class Updates:
- Removed the handling of stdin input from the `HypergoCmd` class.

### hypergo_cli.py Changes:
- Removed the `yaml` import statement, as it is no longer used.
- Added the `json` import statement to support the loading of a JSON configuration.
- Moved the `format_date` and `get_version_path` functions inside the `intro` property getter.
- The `intro` property now displays the version and timestamp of the Hypergo tool.

### hypergo_click.py Changes:
- Renamed the `run` command to `stdio`.
- Removed the `init`, `use`, and `start` commands from the `hypergo_click.py` module.

### hypergo_cmd.py Changes:
- Removed the handling of stdin input from the `HypergoCmd` class.

Note: This diff seems to be a refactor of the Hypergo tool's CLI and input/output handling. The `stdio` method has been added to the `HypergoCli` class to handle standard input/output. Several methods, such as `format_date`, `get_version_path`, `load_config`, `use`, and `start`, have been removed or refactored to support the changes. Additionally, stdin input handling has been removed from various parts of the codebase.

Please note that this release includes internal changes and improvements for the Hypergo tool, making it more robust and efficient. Users of Hypergo can now interact with the tool using standard input/output, and the `HypergoCli` class has been streamlined for better maintainability.

---

### Release Notes - Version X.X.X

#### New Features
- Added a new command-line interface module: `hypergo/hypergo_cli.py`.
  - The `HypergoCli` class provides functionality for interacting with the hypergo system via the command line.
  - Includes commands such as `run`, `use`, `init`, `start`, and `graph` to perform various operations within the system.
- Introduced the `hypergo/hypergo_click.py` module.
  - This module contains a click-based command-line interface for the hypergo system.
  - New commands such as `shell`, `run`, `use`, `init`, `start`, and `graph` are available for easier interaction.

#### Bug Fixes
- Fixed an issue in the `hypergo/hypergo_cmd.py` module, where the `do_exit` method was not properly implemented. It now correctly exits the command-line interface.

#### Dependencies
- Added the following new dependencies in `setup.cfg`:
  - `click`: A Python package for creating command-line interfaces easily.
  - `ansicolors`: A package for adding colored output to the command-line interface.
  - `click-default-group`: A package for setting a default command in click-based command-line interfaces.
  - `graphviz`: A package for working with Graphviz graph visualization software.
  - `urllib3<2.0`: An updated version of urllib3 to address potential compatibility issues.

#### Miscellaneous
- Updated the `install_requires` section in `setup.py` to include the newly added dependencies.

---
Please note that this release may contain additional undocumented changes, improvements, or bug fixes.