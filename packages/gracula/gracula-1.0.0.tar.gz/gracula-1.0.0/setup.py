from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gracula',
    packages=['gracula'],
    version='1.0.0',
    license='MIT',
    install_requires=[],
    author='yutakojima',
    author_email='info@idea-tools.space',
    url='',
    description='very simple twitter api. This package can be done without OAuth.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='python twitter api',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)
