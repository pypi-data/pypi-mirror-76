# read the contents of your README file
from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py37nashiki',
    version='1.0.0',
    find_packages=find_packages,
    author='nashiki',
    authon_email='dev.nassy@gmail.com',
    url='https://github.com/nnashiki/play_py37_package',
    description='This is a test package for me.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_require='==3.7',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Operating System :: MacOS :: MacOS X',
    ]
)
