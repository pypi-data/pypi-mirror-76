"""Main file of YamlBase"""

import argparse
import yaml
import os
from .ybase import YBase
import sys


def main():

    sys.path.append('src/YamlBase')

    parser = argparse.ArgumentParser(description='This utility allows you to manage changes to the database using '
                                                 'configurations')
    parser.add_argument('-cfg_db', action='store', dest='cfg_path',
                        help='Path to yaml file with DB config')
    parser.add_argument('-cfg_action', action='store', dest='action',
                        help='Changes that should be made according config')

    args = parser.parse_args()

    base = YBase(args.cfg_path, args.action)
    base.do_actions()


if __name__ == '__main__':
    main()