import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="nexus-artifact-manager",
    version="1.1.9",
    description="Upload and Download artifact from Nexus v3+ repository",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/stewiejnr/nexus-artifact-manager",
    author="Stewartium",
    author_email="stewartium1@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["nam"],
    include_package_data=True,
    install_requires=["requests", "urllib3"],
    entry_points={
        "console_scripts": [
            "nexus-artifact=nam.__main__:main",
        ]
    },
)
