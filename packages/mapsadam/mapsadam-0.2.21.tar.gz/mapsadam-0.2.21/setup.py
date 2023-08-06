#!/usr/bin/env python3

'''
This package contains a web based GUI for recording video and audio.
'''

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

if __name__ == '__main__':
    setup(
        name = 'mapsadam',
        version = '0.2.21',
        description = 'Analog to Digital Audiovisual Machine',
        long_description = long_description, 
        author = 'John Poncini',
        author_email = 'john@mapsbcorp.com',
        license = 'GPLv2',
        packages = ['adam'],
        include_package_data = True,
        install_requires = ['flask', 'boto3', 'iso3166', 'pyudev'],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Topic :: Multimedia :: Sound/Audio',
            'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
            'Topic :: Multimedia :: Video',
            'Topic :: Multimedia :: Video :: Capture',
       ]
   )
