# confused-argparse

[![Build Status](https://travis-ci.com/cruisen/confused-argparse.svg?branch=master)](https://travis-ci.com/cruisen/confused-argparse)
[![Coverage](https://coveralls.io/repos/github/cruisen/confused-argparse/badge.svg?branch=master)](https://coveralls.io/github/cruisen/confused-argparse?branch=master)
[![Python Version](https://img.shields.io/pypi/pyversions/confused-argparse.svg)](https://pypi.org/project/confused-argparse/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

> Note: VERY Beta, please wait for relase 1.0, since it is not even complete yet

"My standard" goto package for all my scripts/apps. Get argparse cli and configuration management in ONE LINE per parameter ;-) 

With minimal boilerplate to handle:
- System, default and script level configuration management files with *confuse* using *YAML* 
- *OS enviroment* does overwite settings from *YAML*
- Automagic *argparse* CLI creation and handling. Will overwrite all settings from *YAML* and *os enviroment*
- Setting the *logging* level

And:
- Creating the user default and script level *YAML* files at first run
- Optional: Saving state at exit
- and so much more ...

See:
- [confused-argparse](https://pypi.org/project/confused-argparse/) THIS PACKAGE

- [venv](https://docs.python.org/3/library/venv.html) for python virtual enviroment

- [confuse](https://confuse.readthedocs.io/en/latest/) for handling configuration *TOML* files
- [argparse](https://docs.python.org/3/library/argparse.html) for creating a *CLI parser*
- [os.environ](https://docs.python.org/3/library/os.html) for reading *enviroment* variables
- [logging](https://docs.python.org/3/library/logging.html) for *logging* to console
- [YAML](https://en.wikipedia.org/wiki/YAML) for saving configuration data


## Install:
- bash Shell:
```bash
$ python3 -m venv /path/to/new/virtual/environment
$ cd /path/to/new/virtual/environment
$ source ./bin/activate
$ pip install confused-argparse
```

## First Excample
- PROGNAME.py:
```python
import confused-argparse
ca=confused-argparse.set_var()
ca('input_file', str, 'Input file: Read from a local file')
```

Behind the scenes:
- If `input_file` was set in any of the *YAML* files, it will already have a value (Actually views of values, see *confuse*)
- If `input_file` was set in the *os enviroment*, `input_file` will be set accrodingly, overriting the *YAML* setting
- If `--input_file` was set via the *command line* interface with `python3 PROGNAME.py --input_file my_file.txt`, overriting the *YAML* and *os enviroment* setting to *my_file.txt*

In the bash shell:

```bash
$ python3 PROGNAME.py -h

usage: PROGNAME.py [-h] [--input_file INPUT_FILE]

optional arguments:
  -h, --help                  show this help message and exit
  --input_file INPUT_FILE     Input file: Read from a local file
```

---

## Next level:

- PROGNAME.py:
```python
import confused-argparse
ca = confused-argparse.set_var(standard=True, description='My App: Solves a problem')
ca('input_file', str, 'Input file: Read from a local file', group='I/O')
```

Behind the scenes:
- `standard=True`:
  - There are a number of standard argparse options already set, like `--verbose`, `--debug`, `--cron`
  - Scans and read the values defined in the *os enviroment*, case independant, so also the enviroment variable `VERBOSE`
  - For excample: `--verbose` will set the logging level to *INFO*
- `description='My App: Solves a problem'`
  - argparse will print this
- `group='I/O'`:
  - *argparse* will group options with this optional parameter

```bash
$ python3 PROGNAME.py -h

usage: PROGNAME.py [-h] [--input_file INPUT_FILE] [--list_defaults] [--debug] [--verbose] [--cron]

My App: Solves a problem

optional arguments:
  -h, --help                  show this help message and exit

I/O:
  --input_file INPUT_FILE     Input file: Read from a local file [str]=''

Debug options:
Note: Will override 
  --list_defaults             List: List all Vars in dict with there Defaults [bool]=False
  --debug                     Debug: Logging DEBUG Messages (if not --cron, overrides --verbose) [bool]=False
  --verbose                   Verbose: Logging INFO Messages (if not --cron) [bool]=False
  --cron                      Called from Cronjob [bool]=False
```

---

## Want more?

See Documentation. (Soon)


## Pull Requests?

- Will be welcomed, when we reached the first *beta*
- Note: The confused-argparse [github repository](https://github.com/cruisen/confused-argparse) is still private/closed

## DEV
- Supports latest [python3.7+](https://www.python.org/)

- [poetry](https://python-poetry.org/) for managing dependencies and build & publish to [pypy](https://pypi.org/)
- [wemake-python-package](https://github.com/wemake-services/wemake-python-package) for steting up a out of the box ready building enviroment
  - Minor tweaks to `.gitignore` and `Makefile`
- [git](https://en.wikipedia.org/wiki/Git) for version management on [github](https://github.com/)
- [gnu make](https://www.gnu.org/software/make/) for runing tests and building docs

- [jupyter](https://jupyter.org/) for quick tests and some development
- [sphinx](https://www.sphinx-doc.org/en/master/) and [readthedocs.org](https://readthedocs.org/) for documentation
- [travis](https://travis-ci.org/) or [Github Actions](https://github.com/marketplace?type=actions) as the default CI
- [@dependabot](https://dependabot.com/) for always up-to-date dependencies
- [mypy](https://mypy.readthedocs.io/en/stable/) for optional static typing
- [pytest](https://docs.pytest.org/en/stable/) for testing
- [flake8](https://pypi.org/project/flake8/) and [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-package) for linting

## License

[MIT](https://github.com/cruisen/confused-argparse/blob/master/LICENSE)

(c) 2020 Nikolai von Krusenstiern


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [69435b231f7f398474073ac6dd14868dd3edf2c1](https://github.com/wemake-services/wemake-python-package/tree/69435b231f7f398474073ac6dd14868dd3edf2c1). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/69435b231f7f398474073ac6dd14868dd3edf2c1...master) since then.

