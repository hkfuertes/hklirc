#!/usr/bin/python3

import argparse
from lirc_parser import parse as parseLirc
from os import getcwd

KEY_TEMPLATE = '''
begin
    prog   = irexec
    button = <KEY_CODE>
    config = <COMMAND>
end
'''

def generate(filepath):
    lirc = parseLirc('/etc/lirc/lircd.conf.d/')
    available_codes = []
    for key,value in lirc.items():
        for code in value['codes']:
            if(code not in available_codes):
                available_codes.append(code)

    with (open(filepath, "w+")) as f:
        for code in available_codes:
            f.write(KEY_TEMPLATE.replace('<KEY_CODE>', code).replace("<COMMAND>",getcwd() + "/pressKey.py "+ code))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates a LIRC config for all available keys in remotes.')
    parser.add_argument('--config', metavar='config', help=' config file to be created (default in ../all_codes.conf)', default="../all_codes.conf")
    args = parser.parse_args()

    generate(args.config)