"""
pydarts - command line assistant and library for playing darts
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

setup(
        name='pydarts',
        version='0.1',
        description='TODO',
        url='http://github.com/pylipp/pydarts',
        author='Philipp Metzner',
        author_email='beth.aleph@yahoo.de',
        license='GPLv3',
        #classifiers=[],
        packages=find_packages(exclude=['test', 'doc', 'data']),
        entry_points={
            'console_scripts': ['pydarts = pydarts.cli:main']
            },
        install_requires=[]
        )
