import setuptools
from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='cd-utils-logger',
    version='1.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/herculanocm/cd-utils-logger',
    download_url='https://github.com/herculanocm/cd-utils-logger/archive/master.zip',
    license='MIT',
    author='Herculano Cunha',
    author_email='herculanocm@outlook.com',
    description='Utilitário para Log',
    keywords='tools utils logger',
    install_requires=['colorama'],
    python_requires='>=3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
