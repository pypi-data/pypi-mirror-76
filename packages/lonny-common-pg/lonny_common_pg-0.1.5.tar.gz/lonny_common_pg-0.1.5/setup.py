from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "lonny_common_pg",
    version = "0.1.5",
    packages = find_packages(),
    install_requires = requirements
)