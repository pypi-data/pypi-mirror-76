from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "lonny_pg_job",
    version = "1.4",
    packages = find_packages(),
    scripts = ["bin/pg_job"],
    install_requires = requirements
)