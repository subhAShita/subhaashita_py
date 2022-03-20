^[![Build status](https://github.com/subhAShita/subhaashita_py/workflows/Python%20package/badge.svg)](https://github.com/subhAShita/subhaashita_py/actions)
[![Documentation Status](https://readthedocs.org/projects/subhaashita/badge/?version=latest)](http://subhaashita.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/subhaashita.svg)](https://badge.fury.io/py/subhaashita)

## Intro

A package for curating subhAShita-s and quotes. 

## For users
* [Autogenerated Docs on readthedocs (might be broken)](http://subhaashita.readthedocs.io/en/latest/).
* Manually and periodically generated docs [here](https://sanskrit-coders.github.io/subhaashita/build/html/)
* For detailed examples and help, please see individual module files in this package.


## Installation or upgrade:
* For stable version `pip install subhaashita -U`
* For latest code `pip install git+https://github.com/subhAShita/subhaashita_py/@master -U`
* [Web](https://pypi.python.org/pypi/subhaashita).

## For contributors

### Contact

Have a problem or question? Please head to [github](https://github.com/subhAShita/subhaashita_py).

### Packaging

* ~/.pypirc should have your pypi login credentials.
```
python setup.py bdist_wheel
twine upload dist/* --skip-existing
```

### Build documentation
- sphinx html docs can be generated with `cd docs; make html`

#### Testing
Run `pytest` in the root directory.

## Auxiliary tools
- ![Build status](https://github.com/subhAShita/subhaashita_py/workflows/Python%20package/badge.svg)
- [![Documentation Status](https://readthedocs.org/projects/subhaashita/badge/?version=latest)](http://subhaashita.readthedocs.io/en/latest/?badge=latest)
- [pyup](https://pyup.io/account/repos/github/subhAShita/subhaashita_py/)
