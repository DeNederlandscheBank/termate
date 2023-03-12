#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'xlsxwriter', 'rdflib', 'iribaker', 'lxml', 'regex']

test_requirements = ['Click>=7.0', 'xlsxwriter', 'rdflib', 'iribaker', 'lxml', 'nafigator', 'regex']

setup(
    author="Willem Jan Willemse",
    author_email='w.j.willemse@dnb.nl',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Package for terminology management with TermBase eXchange (TBX)",
    entry_points={
        'console_scripts': [
            'termate=termate.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='termate',
    name='termate',
    packages=find_packages(include=['termate', 'termate.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/DeNederlandscheBank/termate',
    version='0.1.11',
    zip_safe=False,
)
