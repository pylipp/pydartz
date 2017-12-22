"""
pydartz - command line assistant and library for playing darts
Copyright (C) 2017 Philipp Metzner

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages
from pydartz import __version__

with open("README.rst") as readme:
    long_description = readme.read()


setup(
        name='pydartz',
        version=__version__,
        description="command line assistant and library for playing darts",
        long_description=long_description,
        url='http://github.com/pylipp/pydartz',
        author='Philipp Metzner',
        author_email='beth.aleph@yahoo.de',
        license='GPLv3',
        keywords='commandline darts',
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Other Audience",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: Unix",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Topic :: Games/Entertainment",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        packages=find_packages(exclude=["test"]),
        entry_points={
            'console_scripts': ['pydartz = pydartz.cli:main']
            },
        install_requires=[],
        data_files=[
            ("data", ["data/chase_the_sun.wav"]),
        ],
        )
