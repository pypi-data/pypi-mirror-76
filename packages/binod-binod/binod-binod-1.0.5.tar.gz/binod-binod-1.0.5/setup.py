import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="binod-binod",
    version="1.0.5",
    description="do something",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tanmay1217/binod",
    author="Tanmay Parashar",
    author_email="parashart98@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["binod3"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "binod=binod3.__main__:main",
        ]
    },
)
