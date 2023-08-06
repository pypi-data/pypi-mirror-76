#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup
from distutils.core import Extension


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


# enable code coverage for C code
# We can't use CFLAGS=-coverage in tox.ini, since that may mess with
# compiling dependencies (e.g. numpy). Therefore we set PY_CCOV=-coverage
# in tox.ini and copy it to CFLAGS here (after deps have been installed)
if 'PY_CCOV' in os.environ.keys():
    os.environ['CFLAGS'] = os.environ['PY_CCOV']


setup(
    name='aacgm2',
    version='2.3.9',
    license='MIT',
    description='A Python wrapper for AACGM-v2 magnetic coordinates',
    long_description='%s\n%s' % (read('README.rst'), re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    long_description_content_type='text/x-rst',
    author='Angeline G. Burrell, Christer van der Meeren',
    author_email='angeline.burrell@nrl.navy.mil',
    maintainer='Stefan Bender',
    maintainer_email='stefan.bender@ntnu.no',
    url='https://github.com/st-bender/aacgmv2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    package_data={'aacgm2': ['aacgm_coeffs/*.asc', 'igrf*coeffs.txt', 'magmodel_*.txt']},
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Utilities',
    ],
    keywords=[
        'aacgm',
        'aacgm-v2',
        'aacgmv2',
        'magnetic coordinates',
        'altitude adjusted corrected geomagnetic coordinates',
        'mlt',
        'magnetic local time',
        'conversion',
        'converting',
    ],
    install_requires=[
        'numpy',
    ],
    ext_modules=[
        Extension('aacgm2._aacgmv2',
                  sources=['src/aacgm2/aacgmv2module.c',
                      'src/c_aacgm_v2/aacgmlib_v2.c',
                      'src/c_aacgm_v2/astalglib.c',
                      'src/c_aacgm_v2/genmag.c',
                      'src/c_aacgm_v2/igrflib.c',
                      'src/c_aacgm_v2/mlt_v2.c',
                      'src/c_aacgm_v2/rtime.c'],
                  extra_compile_args=['-D_USE_MATH_DEFINES'],
                  include_dirs=['src/c_aacgm_v2'])
    ],
    entry_points={
        'console_scripts': [
            'aacgm2 = aacgm2.__main__:main',
        ]
    },
)
