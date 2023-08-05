#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="achraf koulali",
    author_email='achraf.koulali@ncl.ac.uk',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="CEG3707 Practicls",
    entry_points={
        'console_scripts': [
            'ceg3707=ceg3707.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ceg3707',
    name='ceg3707',
    packages=find_packages(include=['ceg3707', 'ceg3707.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/koulali/ceg3707',
    version='0.2.0',
    zip_safe=False,
)
