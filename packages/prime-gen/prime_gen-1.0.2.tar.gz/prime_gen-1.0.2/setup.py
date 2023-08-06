#!/usr/bin/python3
# -*- coding: U8

from setuptools import setup, find_packages

with open('README.md') as fh:
    long_description = fh.read()
setup(
    name='prime_gen',
    version='1.0.2',
    description='A prime generator and checker',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Makonede',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    keywords='python prime math',
    packages=['prime_gen'],
    python_requires='~=3.8'
)
