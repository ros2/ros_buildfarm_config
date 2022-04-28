#!/usr/bin/env python3

import os
import sys

import yaml
import yamlinclude


DIRECTORIES = ['foxy', 'galactic', 'humble', 'rolling']

def main():
    base_path = os.path.dirname(__file__)
    priorities = {}

    for directory in DIRECTORIES:
        current_path = os.path.join(base_path, directory)
        yamlinclude.YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader, base_dir=current_path)

        files = os.listdir(current_path)
        files[:] = [f for f in files if f.endswith('.yaml')]
        files.sort()

        for f in files:
            relpath = os.path.relpath(os.path.join(current_path, f), base_path)
            with open(os.path.join(current_path, f)) as infp:
                data = yaml.load(infp, Loader=yaml.FullLoader)

            for key in sorted(data.keys()):
                if not key.endswith('_priority'):
                    continue
                priority_value = data[key]
                if priority_value not in priorities:
                    priorities[priority_value] = set([])
                priorities[priority_value].add(key + '::' + relpath)

        del yaml.FullLoader.yaml_constructors[yamlinclude.YamlIncludeConstructor.DEFAULT_TAG_NAME]

    for key in sorted(priorities.keys()):
       print(key)
       for value in sorted(priorities[key]):
           print(' ', value)

    return 0


if __name__ == '__main__':
    sys.exit(main())
