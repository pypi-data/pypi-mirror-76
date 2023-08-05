from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "lonny_pg_migrate",
    version = "1.3",
    packages = find_packages(),
    scripts = ["bin/pg_migrate"],
    install_requires = requirements
)