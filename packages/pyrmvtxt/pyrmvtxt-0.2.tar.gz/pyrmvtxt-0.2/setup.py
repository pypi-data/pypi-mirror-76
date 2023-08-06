# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:04:19 2020

@author: supakrni
"""

# In[]
from setuptools import setup

def readme():
    with open('README.txt') as f:
        return f.read()
def licenses():
    with open('LICENSE.txt') as f:
        return f.read()
    
setup(name='pyrmvtxt',
    version='0.2',
    description='Remove text in image',
    long_description=readme(),
    url="",
    author='tasund',
    author_email='supakrit.n@hotmail.com',
    license=licenses(),
    install_requires=[
        'opencv-python',
        'keras-ocr',
        'pandas',
    ],
    keywords='removetextfromimage',
    packages=['pyrmvtxt'],
    package_dir={'pyrmvtxt': 'src/pyrmvtxt'}
)