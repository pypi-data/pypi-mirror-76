# Initme

Utility to help setup python projects and libraries.

## Usages

* Created an `__init__.py` file in every directory containing a python script. Examples: `python -m initme /path/to/my/project` or `cd /path/to/my/project && python -m initme`

## Install

`pip install initme --user`

## Contributing

I started this library because I often have "half baked" python projects which I want to turn into a fully grown library and/or module.

This involves a bunch of annoying boilerplate such as: adding `__init__.py` files everywhere, creating a `setup.py`, creating an `__about__.py` ... etc.

I've created this library to take some of the hassle away from that. Currently it does a single thing, which is created `__init__.py` in every directory with python files, in the future I'd love for it to look at the files content and auto generate:

* A `setup.py`
* An `__about__.py`
* Maybe a simple `.sh` files that helps with deployment or print out some instructions for beginners as to how to go about deploying.
* Change all import's to use the proper module syntax
* Create the "standard" dir structure (e.g. for project `blax` move all "python related" files in a subdir called `blax`)

I'm curios if anyone thinks there's a need for such a library and/or if they want to contribute with the features above or some other ones. It's all fairly easy to do, just requires a bit of time and testing, but I will probably only add the features I need and the ones which other people want.
