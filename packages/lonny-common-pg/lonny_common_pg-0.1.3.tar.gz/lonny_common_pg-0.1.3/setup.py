from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "lonny_common_pg",
    version = "0.1.3",
    packages = find_packages(),
    package_data = { "": [ "requirements.txt" ] },
    include_package_data = True,
    install_requires = requirements
)