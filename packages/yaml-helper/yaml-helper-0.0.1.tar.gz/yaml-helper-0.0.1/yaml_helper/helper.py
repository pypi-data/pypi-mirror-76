import yaml
from yaml import CLoader as Loader, CDumper as Dumper


def load(filename):
    with open(filename) as file:
        return yaml.load(file.read(), Loader=Loader)


def add(filename, config):
    merged = {**load(filename), **config}
    yml = yaml.dump(merged, Dumper=Dumper)

    with open(filename, 'w') as file:
        file.write(yml)
