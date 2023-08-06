#!/usr/bin/env python

from setuptools import setup

VERSION='0.0.4'

with open ('README.rst', 'r') as fh:
    long_description = fh.read ()

with open ('requirements.txt', 'r') as fh:
    requirements = fh.readlines ()

setup (
    name='mapillary-tools',
    version=VERSION,
    description='Mapillary Commandline Image Uploader',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords='mapillary commandline console image upload',
    url='https://github.com/MarcelloPerathoner/mapillary-tools',
    author='Marcello Perathoner',
    author_email='marcello@perathoner.de',
    license='GPL3',
    python_requires='>=3.5.0',
    install_requires=requirements,
    packages=['mapillary_tools'],
    # See: https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
    scripts=[
        'bin/mapillary_auth.py',
        'bin/mapillary_process.py',
        'bin/mapillary_upload.py',
    ],
)
