from setuptools import setup, find_packages

# Read information from package.py to keep in sync with rez
info = {}
with open("package.py") as fp:
    exec(fp.read(), info)

setup(
    name=info["name"],
    version=info["version"],
    author=", ".join(info["authors"]),
    description=info["description"],
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    install_requires=[
        "numpy>=1.23,<2",
        "matplotlib>=3",  # Not actually required but used to find system font paths
    ],
)
