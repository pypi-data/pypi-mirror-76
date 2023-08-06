#!/usr/bin/env python

"""The setup script."""

from os.path import exists

from setuptools import find_packages, setup

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

if exists('README.rst'):
    with open('README.rst') as f:
        long_description = f.read()
else:
    long_description = ''

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Scientific/Engineering',
]

setup(
    name='xpublish',
    description='Publish Xarray Datasets via a REST API.',
    long_description=long_description,
    python_requires='>=3.6',
    maintainer='Joe Hamman',
    maintainer_email='jhamman@ucar.edu',
    classifiers=CLASSIFIERS,
    url='https://github.com/xarray-contrib/xpublish',
    packages=find_packages(exclude=('tests',)),
    package_dir={'xpublish': 'xpublish'},
    include_package_data=True,
    install_requires=install_requires,
    license='MIT',
    zip_safe=False,
    keywords=['xarray', 'zarr', 'api'],
    use_scm_version={'version_scheme': 'post-release', 'local_scheme': 'dirty-tag'},
    setup_requires=['setuptools_scm', 'setuptools>=30.3.0'],
)
