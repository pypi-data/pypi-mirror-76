import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="snaked-py",
    version="1.0.0",
    description="Lightweight high-performance wrapper for accessing camelCase python objects using snake_case syntax.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/squirrel-preslash/snaked",
    author="Squirrel-Preslash",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["snaked"],
    include_package_data=True,
    install_requires=["stringcase"]
)