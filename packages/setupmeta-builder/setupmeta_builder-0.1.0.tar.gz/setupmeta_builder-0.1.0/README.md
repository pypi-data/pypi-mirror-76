# Setupmeta Builder

![GitHub](https://img.shields.io/github/license/Cologler/setupmeta_builder-python.svg)
[![Build Status](https://travis-ci.com/Cologler/setupmeta_builder-python.svg?branch=master)](https://travis-ci.com/Cologler/setupmeta_builder-python)
[![PyPI](https://img.shields.io/pypi/v/setupmeta_builder.svg)](https://pypi.org/project/setupmeta_builder/)

## Usage

Replace your `setup.py` file to:

```py
from setupmeta_builder import setup_it

setup_it()
```

Done!

`setupmeta_builder` try resolve other values like `install_requires` for you.

|meta|resolve source|
|:-|:-|
|`packages`|`find_packages()`|
|`name`|packages|
|`version`|`git.tag`|
|`long_description`|file: `README.[md|rst]`|
|`author` and `author_email`|file: `.pkgit.json`|
|`url`|`git.origin.url`|
|`license`|file: `LICENSE`|
|`classifiers`|license and file `.travis.yml`|
|`install_requires`|files: `requirements.txt` or `pipfile`|
|`tests_require`|file: `pipfile`|
|`extras_require`|files: `requirements.*.txt`|
|`entry_points.console_scripts`|all global functions from file `PACKAGE_ROOT\entry_points_console_scripts.py`|

Current project is the first example.

**You can always print attrs using `python setup.py print_attrs`**

## Details

### entry_points.console_scripts

If your package include a file named `entry_points_console_scripts.py`, setupmeta_builder will exec it and get all item from globals.

So do **NOT** import anything in top of `entry_points_console_scripts.py`.
