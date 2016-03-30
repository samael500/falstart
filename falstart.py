#!/usr/bin/env python

import json
import re
import os
import sys
import argparse
import subprocess
import string
import random

from settings import VARS


def fabric_task(taskname):
    subprocess.call([
        'fab', '-f', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fabfile.py'),
        '--host=localhost', taskname])


def vagrant_fabric():
    """ Check is vagrant fabric installed and if not - install """
    plugins = subprocess.check_output(['vagrant', 'plugin', 'list'])
    if 'vagrant-fabric' not in plugins:
        subprocess.call(['vagrant', 'plugin', 'install', 'vagrant-fabric'])


def str_random(size=9, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    """ Not a fabric task, it will generate random str for passw """
    return ''.join(random.choice(chars) for _ in range(size))


def from_user(msg, default, validate, yesno=False):
    """ Get value from user """
    if VARS.get('no_input'):
        return default
    while True:
        value = raw_input('\033[1m{}\033[0m\tdefault "{}" '.format(msg, 'nY'[default] if yesno else default)).strip()
        if not value and default is not None:
            return default
        if re.match(validate, value):
            if yesno:
                return value.lower() == 'y'
            return value
        print '\033[1mInvalide\033[0m'


def read_data(args):
    VARS.update(args)
    VARS['base_path'] = os.getcwd()

    root_dir = VARS.get('root_dir', '')
    proj_name = VARS.get('proj_name') or ''.join(re.split(r'[^a-z]', root_dir.lower()))
    VARS['proj_name'] = proj_name or from_user('Enter a project name', proj_name, re.compile(r'^[a-z0-9]+$'))

    proj_ip = VARS.get('proj_ip', '10.1.1.123')
    VARS['proj_ip'] = from_user('Vagrant box IP-addr\t', proj_ip, re.compile(r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'))

    for name in 'POSTGRES', 'CELERY', 'REDIS':
        value = VARS.get(name, False)
        VARS[name] = from_user(
            'Do you nead a {} Y/n'.format(name) + ('\t' if name in ('REDIS', ) else ''),
            value, re.compile(r'^[YyNn]{1}$'), yesno=True)

    print ''

    for name in ('db_name', 'db_user', 'db_pass'):
        value = VARS.get(name)
        default = '{proj_name}_{}'.format(['db', 'user'][name == 'db_user'], **VARS)
        if name == 'db_pass':
            default = str_random()
        VARS[name] = from_user(
            'Database {}'.format(name).replace('db_', ''), value or default, re.compile(r'^\w+$'))

    VARS['root_dir'] = os.path.join(VARS['base_path'], VARS['root_dir'])


def parse():
    parser = argparse.ArgumentParser(description='Falstart is a fast develop template box start tool.')
    parser.add_argument('root_dir', nargs='?', help='Name of started project', type=str)
    parser.add_argument(
        '--no-input', dest='no_input', action='store_true',
        help='Non interactive config parse', default=False)
    return parser.parse_args().__dict__

def presettings():
    """ Call user to insert required settings """

def main():
    read_data(parse())
    json.dump(VARS, open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cfg.json'), 'w'))
    fabric_task('common:start_box')


if __name__ == '__main__':
    vagrant_fabric()
    main()
