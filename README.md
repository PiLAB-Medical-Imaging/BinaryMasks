# Binary Masks Operations

Welcome to the Binary Masks Operations's Github repository! 

## Description

This package contains helpful functions enabling a faster clean up of binary masks and other functionalities.


## Installing & importing

### Online install

The BinaMa package is available through ```pip install``` under the name ```pilab-binama```. Note that the online version might not always be up to date with the latest changes.

```
pip install pilab-binama
```
To upgrade the current version : ```pip install pilab-binama --upgrade```.

To install a specific version of the package use
```
pip install pilab-binama==0.0.2
```
All available versions are listed in [PyPI](https://pypi.org/project/pilab-binama/). The package names follow the rules of [semantic versioning](https://semver.org/).

### Local install

If you want to download the latest version directly from GitHub, you can clone this repository
```
git clone https://github.com/PiLAB-Medical-Imaging/BinaryMasks
```
For a more frequent use of the library, you may wish to permanently add the package to your current Python environment. Navigate to the folder where this repository was cloned or downloaded (the folder containing the ```setup.py``` file) and install the package as follows
```
cd binama
pip install .
```

If you have an existing install, and want to ensure package and dependencies are updated use --upgrade
```
pip install --upgrade .
```
### Importing
At the top of your Python scripts, import the library as
```
import binama.utils as bm
```

### Checking current version installed

The version of the TIME package installed can be displayed by typing the following command in your python environment
```
binama.__version__
``` 

### Uninstalling
```
pip uninstall pilab-binama
```

## Example data and code

An example use of the main methods and outputs of BinaMa is written in the `example.py` file.
