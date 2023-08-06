"""Main file of YamlBase"""

import argparse
import yaml
import os
from YamlBase.ybase import YBase
import sys
import os


def main():

    os.chdir('../../')

    parser = argparse.ArgumentParser(description='This utility allows you to manage changes to the database using '
                                                 'configurations')
    parser.add_argument('-cfg_db', action='store', dest='cfg_path',
                        help='Path to yaml file with DB config')

    args = parser.parse_args()
    print(os.listdir())
    base = YBase('base_example.yml')
    base.do_actions()


if __name__ == '__main__':
    main()