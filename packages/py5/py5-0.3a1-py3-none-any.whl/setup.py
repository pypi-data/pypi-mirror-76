from pathlib import Path
from setuptools import setup

with open('README.rst') as f:
    README = f.read()


with open(Path('py5', '__init__.py')) as f:
    for line in f.readlines():
        if line.startswith('__version__'):
            break
    VERSION = line.split("'")[-2]


setup(
    name='py5',
    version=VERSION,
    packages=['py5'],
    py_modules=['setup'],
    python_requires='>3.8',
    description='Processing for CPython',
    long_description=README,
    author='Jim Schmitz',
    author_email='jim@ixora.io',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.8',
    ],
)
