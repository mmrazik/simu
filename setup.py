from distutils.code import setup
from setuptools import find_packages
import os


def get_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory)]

setup(
    name='simu',
    version='1.0',
    packages=find_packages(),
    test_suite='tests',
    scripts=[
        'bin/simu-remote',
    ],
    data_files=[('/var/www/simu', get_files('www'))],
)
