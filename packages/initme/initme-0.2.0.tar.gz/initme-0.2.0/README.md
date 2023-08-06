# Initme

Utility to help setup python projects and libraries.

## Usages

* Created an `__init__.py` file in every directory containing a python script. Examples: `python -m initme /path/to/my/project` or `cd /path/to/my/project && python -m initme`

## Install

`pip install initme --user`

## Contributing

I started this library because I often have "half baked" python projects which I want to turn into a fully grown library and/or module.
This involves a bunch of annoying boilerplate such as: adding `__init__.py` files everywhere, creating a `setup.py`, creating an `__about__.py` ... etc
