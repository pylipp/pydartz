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
        packages=find_packages(exclude=['test', 'doc']),
        entry_points = {
            'console_scripts': ['pydarts = pydarts.main:main']
            },
        install_requires=[]
        )
