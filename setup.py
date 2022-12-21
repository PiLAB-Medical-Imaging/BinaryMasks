from setuptools import setup

import binama

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pilab-binama',
    version=binama.__version__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/PiLAB-Medical-Imaging/BinaryMasks',
    author='PiLAB',
    author_email='nicolas.delinte@uclouvain.be',
    license='GNU General Public License v3.0',
    packages=['binama'],
    install_requires=['numpy',
                      'scikit-image',
                      ],

    classifiers=['Natural Language :: English',
                 'Programming Language :: Python'],
)
