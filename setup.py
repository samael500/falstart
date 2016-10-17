# -*- coding: utf-8 -*-

import io
import os
import re

from setuptools import setup


version = re.search('^__version__\s*=\s*"(.*)"', open('falstart/__init__.py').read(), re.M).group(1)


def read(fname):
    return io.open(os.path.join(os.path.dirname(__file__), fname), encoding='UTF-8').read()


with open('requirements.txt') as requf:
    required = requf.read().splitlines()


setup(
    name='falstart',
    version=version,
    author='Maks Skorokhod',
    author_email='samae500@gmail.com',
    url='https://github.com/Samael500/falstart',
    packages=['falstart'],
    package_data={
        'falstart': [
            'templates/*.j2',
            'templates/py_codes/*.j2',
            'templates/includes/*.j2',
            'templates/vagrant_templates/*.j2',
        ]
    },
    license='MIT',
    description='Tool for fast start develop box template.',
    long_description=read('README.rst'),
    install_requires=required,
    data_files=[('', ['LICENSE', 'README.rst', ]), ],
    entry_points={
        'console_scripts': ['falstart = falstart.falstart:main']
    },
    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords='falstart fabric vagrant virtualbox development fast start template'.split(),
)
