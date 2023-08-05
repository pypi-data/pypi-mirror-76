# -*- coding: utf-8 -*-
"""Setup configuration."""
from setuptools import find_packages
from setuptools import setup


setup(
    name="immutable_data_validation",
    version="0.2.1",
    description="Validating basic Python data types.",
    url="https://github.com/CuriBio/immutable-data-validation",
    author="Curi Bio",
    author_email="contact@curibio.com",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["validator-collection>=1.3.5"],
)
