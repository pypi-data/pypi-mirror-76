from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Encod",
    version="0.0.7",
    description="A Python package to encode and decode with style.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/pisslow/styleEncoder/",
    author="pisslow",
    author_email="pisslowmail@gmail.com",
    license="MIT",
    packages=["encoding"]
)