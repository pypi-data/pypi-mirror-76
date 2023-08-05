# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

dependencies = [
        'numpy>=1.16.2',
        'scipy>=1.2.1',
        'matplotlib>=3.0.3',
        'autograd>=1.3',
        'pyMKL>=0.0.3'
]

setup(
    name='ceviche',
    version='0.1.2',
    description='Ceviche',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Tyler Hughes',
    author_email='tylerwhughes91@gmail.com',
    url='https://github.com/twhughes/ceviche',
    packages=find_packages(),
    install_requires=dependencies,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
