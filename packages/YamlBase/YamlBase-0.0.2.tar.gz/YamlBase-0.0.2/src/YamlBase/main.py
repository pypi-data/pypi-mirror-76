"""Main file of YamlBase"""

import argparse
import yaml
from ybase import YBase

if __name__ == '__main__':

    with open('descriptions_cfg.yaml') as f:
        descriptions = yaml.load(f)

    parser = argparse.ArgumentParser(description=descriptions['arg_parse_descr'])
    parser.add_argument('-cfg_db', action='store', dest='cfg_path',
                        help='Path to yaml file with DB config')
    parser.add_argument('-cfg_action', action='store', dest='action',
                        help='Changes that should be made according config')

    args = parser.parse_args()

    a = YBase(args.cfg_path)

    print(a.insert_action())
