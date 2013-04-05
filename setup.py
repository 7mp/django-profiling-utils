#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(name='Django profiling utils',
    version=".".join(map(str, __import__("profiling_utils").__version__)),
    description='Django profiling utils',
    author='Tommi Penttinen',
    author_email='tommi.penttinen@iki.fi',
    maintainer='Tommi Penttinen',
    maintainer_email='tommi.penttinen@iki.fi',
    url='http://github.com/7mp/django-profiling-utils/',
    packages=find_packages(),
    #install_requires=['django>=1.3'],
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
)
