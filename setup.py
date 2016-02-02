"""
Setup script for dgi_repo.
"""

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='dgi_repo',
    version='1.x',
    description="discoverygarden's repository software",
    author='discoverygarden',
    author_email='dev@discoverygarden.ca',
    license='TBD',
    packages=find_packages(),
    package_dir={'dgi_repo': 'dgi_repo'},
    package_data={'dgi_repo': ['resources/*.*']},
    long_description=read('README.md'),
    install_requires=[
        'falcon',
        'talons',
        'falcon-multipart',
        'lxml',
        'psycopg2',
        'pyyaml'
    ],
    dependency_links=[
        'git+https://github.com/yohanboniface/falcon-multipart.git@2acabc96dc64b01404f455d3f957f9b98dc0b1ae#egg=falcon_multipart-0.1.0'
    ]
)
