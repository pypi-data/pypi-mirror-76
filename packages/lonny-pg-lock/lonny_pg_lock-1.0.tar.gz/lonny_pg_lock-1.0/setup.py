from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "lonny_pg_lock",
    version = "1.0",
    packages = find_packages(),
    install_requires = requirements
)