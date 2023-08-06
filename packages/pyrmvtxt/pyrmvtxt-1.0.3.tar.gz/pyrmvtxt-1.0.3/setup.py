# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:04:19 2020

@author: supakrni
"""

from setuptools import setup

def readme():
    with open('README.txt') as f:
        return f.read()
#def licenses():
#    with open('LICENSE.txt') as f:
#        return f.read()
    
setup(name='pyrmvtxt',
    version='1.0.3',
    description='Remove text in image',
    long_description=readme(),
    url="",
    author='tasund',
    author_email='supakrit.n@hotmail.com',
    license='MIT License Copyright  2020 TASUNDPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the Software), to deal in the Software without restriction,including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DINGS IN THE SOFTWARE.',
    install_requires=[
        'opencv-python',
        'keras-ocr',
        'pandas',
    ],
    keywords='removetextfromimage',
    packages=['pyrmvtxt'],
    package_dir={'pyrmvtxt': 'src/pyrmvtxt'}
)