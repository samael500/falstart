#!/usr/bin/env python

import re
import argparse
import subprocess
import string
import random

from .settings import VARS
from .local_provision import common


def vagrant_fabric():
    """ Check is vagrant fabric installed and if not - install """
    plugins = subprocess.check_output(['vagrant', 'plugin', 'list'])
    if 'vagrant-fabric' not in plugins:
        # https://github.com/wutali/vagrant-fabric
        subprocess.call(['vagrant', 'plugin', 'install', 'vagrant-fabric'])


def str_random(size=9, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    """ Not a fabric task, it will generate random str for passw """
    return ''.join(random.choice(chars) for _ in range(size))


def from_user(msg, default, validate, yesno=False):
    """ Get value from user """
    message = '\033[1m> {}\033[0m [{}] '.format(msg, ('y/N', 'Y/n')[default] if yesno else repr(default))
    validator = re.compile(validate)
    if VARS.get('no_input'):
        return default
    while True:
        value = raw_input(message).strip()
        if not value and default is not None:
            return default
        if re.match(validator, value):
            if yesno:
                return value.lower() == 'y'
            return value
        print('\033[31m\033[1m> Incorrect input format\033[0m\033[31m check regex r"{}"\033[0m'.format(validate))


def read_data(args):
    VARS.update(args)

    proj_name = ''.join(re.split(r'[^a-z]', (VARS.get('root_dir') or 'test').lower()))
    VARS['proj_name'] = proj_name or from_user(
        'Enter a project name', proj_name, r'^[a-z]+([a-z]|\d)*$')
    if not VARS.get('root_dir'):
        VARS['root_dir'] = VARS['proj_name']

    VARS['dj_version'] = from_user(
        'Django version', VARS.get('dj_version'), r'^([0-9]{1,2}\.){1,2}[0-9]{1,2}$')

    while True:
        py_version = from_user(
            'Python version', VARS.get('py_version'), r'^([0-9]{1,2}\.){1,2}[0-9]{1,2}$')

        if subprocess.check_output([
                'curl', '-sL', 'https://www.python.org/ftp/python/{py_version}/'.format(py_version=py_version),
                '-w', '%{http_code}', '-o', '/dev/null']) == '200':

            VARS.update(dict(py_version=py_version, pyenv_version=re.findall(r'^\d{1,2}\.\d{1,2}', py_version)[0]))
            break
        print(
            '\033[31m\033[1m> Python version "{py_version}" not available\033[0m\033[31m '
            'check uri https://www.python.org/ftp/python/\033[0m').format(py_version=py_version)

    VARS['proj_ip'] = from_user(
        'Vagrant box IP-addr', VARS.get('proj_ip'), r'^([0-9]{1,3}\.){3}[0-9]{1,3}$')

    for name in 'POSTGRES', 'CELERY', 'REDIS':
        VARS[name] = from_user(
            'Do you nead a {}?'.format(name), VARS.get(name, False), r'^[YyNn]{1}$', yesno=True)

    if VARS.get('POSTGRES'):
        for name in ('db_name', 'db_user', 'db_pass'):
            default = '{proj_name}_{}'.format(['db', 'user'][name == 'db_user'], **VARS)
            if name == 'db_pass':
                default = str_random()
            VARS[name] = from_user(
                'Database {}'.format(name).replace('db_', ''), VARS.get(name) or default, r'^\w+$')


def parse():
    parser = argparse.ArgumentParser(description='Falstart is a fast develop template box start tool.')
    parser.add_argument('root_dir', nargs=1, help='Name of started project', type=str)
    parser.add_argument(
        '--no-input', dest='no_input', action='store_true',
        help='Non interactive config parse', default=False)
    parser.add_argument(
        '--box', dest='custom_box', action='store_true',
        help='Pack vagrant to custom box', default=False)
    result = parser.parse_args().__dict__
    result['root_dir'] = result['root_dir'][0]
    return result


def main():
    vagrant_fabric()
    parse_data = parse()
    if parse_data['custom_box']:
        common('make_custom_box', parse_data['root_dir'])
    else:
        read_data(parse_data)
        common('start_box', parse_data['root_dir'], VARS)
