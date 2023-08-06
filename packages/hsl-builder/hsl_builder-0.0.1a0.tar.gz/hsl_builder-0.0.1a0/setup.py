from setuptools import setup,find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hsl_builder',
    version='0.0.1-alpha',
    description='HSL Builder for creating hsl elements',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=('tests',)),
    zip_safe=False,
    url="https://github.com/hellohaptik/python-hsl")
