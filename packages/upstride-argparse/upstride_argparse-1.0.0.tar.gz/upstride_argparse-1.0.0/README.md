# Upstride argument parser

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/UpStride/betterargparse.svg?branch=master)](https://travis-ci.org/github/UpStride/betterargparse)


This package provides a simple and efficient argument parser for every python projects. The idea is to define once all the arguments and then be able to parse 
them from the command line or configuration files

## Example

Let's start with a simple example to demonstrate how it works :

let's create a file `app.py` containing : 
```python
import upstride_argparse as argparse

arguments = [
    [int, "batch_size", 128, 'The size of batch per gpu', lambda x: x > 0],
    [bool, "cpu", False, 'run on cpu'],
    [str, 'description', '', 'description of the experiment'],
    [float, "lr", 0.0001, 'learning rate', lambda x: x > 0],
    ['list[int]', "raw_size", [256, 256, 3], 'raw shape of one image'],
    ['list[str]', "yaml_config", [], "config files"]
]

config = argparse.parse_cmd(arguments)
print(config)
```

so as you can see, the arguments are defined using a standard python list containing lists of `[type, name, default, help, condition]`
  - type can be a python type (`int`, `bool`, `str`, `float`) or a string `list[python_type]` for processing lists
  - condition is a function called when the parameters will be parsed. if one parameter doesn't respect the condition, an exception will be raised.

Now let's try to call this program
- `python app.py` prints `{'batch_size': 128, 'cpu': False, 'description': '', 'lr': 0.0001, 'raw_size': [256, 256, 3], 'yaml_config': []}`. This dictionary contains the default configuration
- `python app.py --cpu --lr 0.1 --description hello --raw_size 28 28 1` prints `{'batch_size': 128, 'cpu': True, 'description': 'hello', 'lr': 0.1, 'raw_size': [28, 28, 1], 'yaml_config': []}`

now lets create a yaml file `config.yml` containing :
```yaml
batch_size: 16
cpu: true
```

- `python app.py --yaml_config config.yml` prints `{'batch_size': 16, 'cpu': True, 'description': '', 'lr': 0.0001, 'raw_size': [256, 256, 3], 'yaml_config': []}`
- `python app.py --yaml_config config.yml --cpu false` prints `{'batch_size': 16, 'cpu': False, 'description': '', 'lr': 0.0001, 'raw_size': [256, 256, 3], 'yaml_config': []}`

as you can see, the command line has the priority over the configuration file

It is also possible to split the configuration between as many configuration file as you want

## Namespaces

For larger project, it can become useful to define namespaces to organized the configuration. This can be done like this : 

```python
import upstride_argparse as argparse

arguments = [
    [int, "batch_size", 128, 'The size of batch per gpu', lambda x: x > 0],
    ['list[str]', "yaml_config", [], "config files"],
    ['namespace', 'first_namespace', [
        [str, 'arg1', 'hello', 'first argument'],
        ['namespace', 'second_namespace', [
            [bool, "i_am_not_doing_anything", True, ''],
            [bool, "nether_do_i", False, '']
        ]],
    ]],
]

config = argparse.parse_cmd(arguments)
print(config)
```

- calling `python app.py` will print `{'batch_size': 128, 'yaml_config': [], 'first_namespace': {'arg1': 'hello', 'second_namespace': {'i_am_not_doing_anything': True, 'nether_do_i': False}}}`

variable from namespace can be configure from yaml config file this way :

```yaml
batch_size: 16
first_namespace:
  arg1: world
  second_namespace:
    i_am_not_doing_anything: false
    nether_do_i: true
```

- calling `python app.py --yaml_config config.yml` will print `{'batch_size': 16, 'yaml_config': [], 'first_namespace': {'arg1': 'world', 'second_namespace': {'i_am_not_doing_anything': False, 'nether_do_i': True}}}`

and these variables can be setup from the command line like this : `python app.py --yaml_config config.yml --first_namespace.arg1 bob --first_namespace.second_namespace.i_am_not_doing_anything false`

it will print : `{'batch_size': 16, 'yaml_config': [], 'first_namespace': {'arg1': 'bob', 'second_namespace': {'i_am_not_doing_anything': False, 'nether_do_i': True}}}`