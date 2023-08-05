from setuptools import setup
from pypi_packaging import _LOCAL_PYPI_VERSION

with open('./README.md', 'r') as file:
    long_description = file.read()

setup(
    name="cumason123-helloworld",
    summary="Example automated pypi packaging",
    long_description_content_type="text/markdown",
    long_description=long_description,
    home_page="http://cumason.me/",
    author="Curtis Mason",
    author_email="cumason@bu.edu",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    package_dir={'':'src'},
    packages=["helloworld"],
    version=_LOCAL_PYPI_VERSION
)
