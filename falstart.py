#!/usr/bin/env python

import os
import subprocess

from .settings import settings


def run():
    settings['base_path'] = os.getcwd()
    subprocess.call(['fab', '-f', './fabfile.py', '--host=localhost', 'common'])


if __name__ == '__main__':
    run()
