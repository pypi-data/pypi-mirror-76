# List Manager
[![Build Status](https://travis-ci.org/nairraghav/lists-library.svg?branch=master)](https://travis-ci.org/nairraghav/lists-library)
[![codecov.io](https://codecov.io/github/nairraghav/lists-library/coverage.svg?branch=master)](https://codecov.io/gh/nairraghav/lists-library)
[![PyPI version](https://badge.fury.io/py/list-manager.svg)](https://badge.fury.io/py/list-manager)

A CLI tool that allows for list management


## How To Use
This tool is meant to be used as a CLI (command line interface). You will need to install the package from pypi
```bash
pip install list_manager
```

After installing, you can immediately start using the tool from your command line

### Show All Lists
```bash
list_manager get_lists
```

### Show All Items In List
```bash
list_manager get_list -l <list-name>
```

### Create List
```bash
list_manager create_list -l <list-name> -i <optional-initial-list-item>
```

### Add Item To List
```bash
list_manager add_item -l <list-name> -i <item-name>
```

### Delete Item From List
```bash
list_manager delete_item -l <list-name> -i <item-name>
```

### Delete List
```bash
list_manager delete_list -l <list-name>
```
