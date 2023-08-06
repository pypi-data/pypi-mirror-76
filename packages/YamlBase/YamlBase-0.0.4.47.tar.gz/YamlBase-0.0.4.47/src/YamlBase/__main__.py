"""Main file of yamlbase"""

import argparse
import yaml
import os
from ybase import YBase
from yaml_worker import YamlActionsWorker

import sys


def main():
    sys.path.append('src/yamlbase')

    with open('src/yamlbase/descriptions_cfg.yaml') as f:
        descriptions = yaml.load(f)

    parser = argparse.ArgumentParser(description=descriptions['arg_parse_descr'])
    parser.add_argument('-cfg_db', action='store', dest='cfg_path',
                        help='Path to yaml file with DB config')
    parser.add_argument('-cfg_action', action='store', dest='action',
                        help='Changes that should be made according config')

    args = parser.parse_args()

    base = YBase(args.cfg_path, args.action)
    base.do_actions()


if __name__ == '__main__':
    raise SystemExit(main())