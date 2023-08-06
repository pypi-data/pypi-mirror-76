# YAML Helper

Helper methods to read and write `.yml` files.

## Installation
`pip install yaml-helper`

## Usage
```
import yaml_helper as yaml


yml_file = 'config.yml'
yml = yaml.load(yml_file)
additional = {'driver': 'mysqli'}

yaml.add(additional)
```
