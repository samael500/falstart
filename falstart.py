#!/usr/bin/env python

import os
import sys
import subprocess


def run():
    common = 'common'
    if len(sys.argv) > 1:
        common += ':{}'.format(sys.argv[1])
    subprocess.call([
        'fab', '-f', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fabfile.py'),
        '--host=localhost', common])


if __name__ == '__main__':
    run()
