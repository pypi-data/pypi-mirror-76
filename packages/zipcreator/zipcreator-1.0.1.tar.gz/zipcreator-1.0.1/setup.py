from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='zipcreator',
    url='https://github.com/mpalazzolo/zipcreator',
    version='1.0.1',
    packages=['zipcreator'],
    license='LICENSE.txt',
    author='Matt Palazzolo',
    author_email='mattpalazzolo@gmail.com',
    description='A quick tool for creating a zipfile from a list of files and/or directories.',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
