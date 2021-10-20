from setuptools import setup,find_packages
setup(
    name="nanopsu",
    version="1.0",
    # python_requires=">=3.6",
    description="Nanopore pseudouridine sequencing",
    author="Sihao Huang",
    packages=find_packages(),
    include_package_data=True,
    scripts=["bin/nanopsu"],
    license="GPL 3.0"
)