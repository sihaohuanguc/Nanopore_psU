from setuptools import setup,find_packages
setup(
    name="nanopsu",
    version="1.0",
    description="Nanopore pseudouridine sequencing",
    author="Sihao Huang",
    packages = find_packages(),
    scripts=["bin/nanopsu"],
    license="GPL 3.0"
)