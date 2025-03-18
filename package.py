# rez package configuration
name = "met_viewport_utils"
version = "0.1.4"
authors = ["alex.telford"]
description = "minimaleffort.tech generic viewport utilities for python based DCCs"
requires = [
    "python-3.9+<3.12",
    "numpy-1.23+<2",
    "~matplotlib-3+",  # TODO: Remove, this is only used to find system font paths
]
build_requires = [
    "python-3.9+<3.12",
]
tools = []
variants = []
build_command = "python {root}/build.py {install}"

tests = {}  # TODO

def commands():
    env.PYTHONPATH.append("{this.root}/python")
