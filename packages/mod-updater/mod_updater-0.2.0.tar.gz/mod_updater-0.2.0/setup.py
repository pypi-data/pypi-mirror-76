import io
import os

from setuptools import find_packages, setup

NAME = 'mod_updater'
DESCRIPTION = 'Automatically update forge minecraft mods'
URL = 'https://github.com/snallapa/mod_updater'
EMAIL = 'sahith.reddy@gmail.com'
AUTHOR = 'Sahith Nallapareddy'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.2.0'

REQUIRED = [
    'requests', 'tqdm'
]

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    entry_points={
        'console_scripts': ['mod_updater=mod_updater.mod_updater:main'],
    },
    install_requires=REQUIRED,
    extras_require={},
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent"
    ],
)