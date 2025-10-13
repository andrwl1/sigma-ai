from setuptools import setup, find_packages
setup(
    name="sigma-ai",
    version="3.0.0",
    package_dir={"": "scripts/python"},
    packages=find_packages(where="scripts/python"),
    install_requires=["matplotlib"],
)
