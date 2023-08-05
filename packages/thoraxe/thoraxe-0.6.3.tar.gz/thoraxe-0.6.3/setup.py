#!/usr/bin/env python

import os
from setuptools import setup, find_packages

with open(os.path.join("thoraxe", "version.py")) as file:
    exec(file.read())

setup(
    name='thoraxe',
    description="Disentangle homology relationships between exons.",
    keywords=['orthologous exons', 'protein isoforms', 'gene transcripts'],
    author="Diego Javier Zea, Hugues Richard & Elodie Laine",
    author_email='diegozea@gmail.com',
    url='https://github.com/PhyloSofS-Team/thoraxe',
    version=__version__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English', 'Programming Language :: Python :: 3'
    ],
    python_requires=">=3.6.1",  # pandas
    entry_points={
        'console_scripts': [
            'transcript_query=thoraxe.transcript_query:main',
            'thoraxe=thoraxe:main'
        ],
    },
    packages=find_packages(),
    package_data={'thoraxe': ['subexons/assets/cluster_plots.html']},
    setup_requires=['pytest-runner'],
    install_requires=[
        'pandas>0.21.0', 'biopython>1.44,<1.78', 'requests', 'numpy<1.20', 'recordclass',
        'urllib3', 'networkx'
    ],
    test_suite='tests',
    tests_require=[
        'pytest', 'pytest-cov', 'coveralls', 'codecov', 'pytest-pylint',
        'pylint'
    ],
    include_package_data=True,
    zip_safe=False,
    license="MIT license")
