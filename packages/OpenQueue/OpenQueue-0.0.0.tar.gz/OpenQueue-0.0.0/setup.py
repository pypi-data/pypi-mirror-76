import os
import re


from setuptools import setup


NAME = "OpenQueue"


def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()


def get_data(var):
    with open(os.path.join(NAME, "__init__.py")) as f:
        return re.search(
            "{} = ['\"]([^'\"]+)['\"]".format(var), f.read()
        ).group(1)


setup(
    name=NAME,
    version=get_data("__version__"),
    url=get_data("__url__"),
    description=get_data("__description__"),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author=get_data("__author__"),
    author_email=get_data("__author_email__"),
    install_requires=get_requirements(),
    license='GPL v3',
    packages=['OpenQueue'],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False
)
