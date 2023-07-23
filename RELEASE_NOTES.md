## Release Notes - Version X.Y.Z

### New Features and Enhancements
- Added a new utility function `traverse_datastructures` in the `hypergo.utility` module. This function allows traversing through nested data structures such as dictionaries and lists and applies a transformation function on each element, enabling easier serialization and deserialization of complex data structures.

### Changes to Existing Functionality
- Modified the `hypergo.transform.Transform.serialization` method to use the new `traverse_datastructures` utility function for serialization, improving the serialization process for nested data structures.

### Bug Fixes
- Fixed an issue in the `hypergo.utility.deserialize` function, where binary data and bytes were not being deserialized correctly. The function now properly deserializes binary data and bytes.

### Testing
- Expanded the test suite in `tests.test_utility_serialization.py` to include comprehensive tests for various data types and nested data structures.
- Added a new test method `test_comprehensive_dict` in `tests.test_utility_serialization.py`, which tests the serialization and deserialization of a comprehensive dictionary containing various data types, nested dictionaries, lists, functions, classes, and instances.
- The test suite now achieves higher code coverage and ensures more robustness of the serialization and deserialization process.

### Miscellaneous
- Updated the `hypergo.utility.serialize` and `hypergo.utility.deserialize` methods to handle edge cases and improve the overall reliability of the serialization and deserialization process.

### Deprecations and Removals
- None.

### Internal Refactorings
- Internal optimizations and code refactorings for improved maintainability and performance.

### Known Issues
- None.

### Contributors
- Thanks to [Contributor Name](mailto:contributor@example.com) for their valuable contributions to this release.

### Note
- Please update your code to use the new `traverse_datastructures` utility function for serialization and deserialization of nested data structures to ensure compatibility with the latest version.

---

# Release Notes - Version X.Y.Z

## New Features

- Added `sdk unit tests` decorator which automates testing in the linter.
- Added more decorators for `validation`, `compression`, and `encryption`.

## Changes

- The `Executor` class in `hypergo/executor.py` now includes a new method `execute` with the `Transform.serialization` decorator, allowing for serialization of function objects.

## Dependencies

- Added `dill` as a new dependency.

Please note that this is just a summary of the changes made. For more detailed information, you can refer to the individual files and their corresponding commits.

# Release Notes

## Version X.Y.Z (Date)

### Bug Fixes

- Fixed a bug in `hypergo/config.py` that caused an issue with importing the `NotRequired` type.
- Fixed a bug in `hypergo/executor.py` where input bindings were not formatted correctly.

### Removed Code

- Removed the `Config` class from `hypergo/config.py`.
- Removed the `load_configs` function from `hypergo/graph.py`.

### Refactoring

- Refactored the `ConfigType` class in `hypergo/config.py` to use the `TypedDictType` from `hypergo/custom_types.py`.
- Refactored the `from_yaml` and `from_json` methods in `Config` class from `hypergo/config.py`.
- Refactored the `graph` function in `hypergo/graph.py` to load multiple configuration files.

### Miscellaneous

- Updated dependencies: `typing_extensions` to `NotRequired` in `hypergo/config.py`.
- Improved error handling in `hypergo/hypergo_cli.py` when executing commands.

### Removed Unused Imports

- Removed unused imports from `hypergo/config.py`.
- Removed unused imports from `hypergo/hypergo_cli.py`.
- Removed unused imports from `hypergo/hypergo_click.py`.

### Updated CLI Output

- Updated the CLI output in `hypergo/hypergo_cli.py` to show version information and prompt.

### Performance Improvements

- Improved performance in `hypergo/hypergo_cmd.py` by handling recognized commands efficiently.

### Documentation Updates

- Updated documentation in `hypergo/config.py` to reflect changes and add missing comments.
- Updated the `graph` function documentation in `hypergo/graph.py`.
- Updated documentation in `hypergo/message.py`.
- Updated the `consume` method documentation in `hypergo/stdio_connection.py`.

### Code Clean-Up

- Cleaned up unused code and commented-out code from several files.


---

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