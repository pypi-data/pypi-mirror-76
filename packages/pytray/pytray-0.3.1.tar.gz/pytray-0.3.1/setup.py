# -*- coding: utf-8 -*-
from setuptools import setup

__author__ = "Martin Uhrin"
__license__ = "GPLv3"

about = {}
with open('pytray/version.py') as f:
    exec(f.read(), about)

setup(name="pytray",
      version=about['__version__'],
      description='A python tools library for baking pies',
      long_description=open('README.rst').read(),
      url='https://github.com/muhrin/pytray.git',
      author='Martin Uhrin',
      author_email='martin.uhrin.10@ucl.ac.uk',
      license=__license__,
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      keywords='tools utilities',
      install_requires=['async_generator', 'deprecation'],
      python_requires=">=3.5",
      extras_require={
          'dev': [
              'grayskull',
              'pip',
              'pre-commit~=2.2;python_version>"3.5"',
              'pre-commit~=1.21;python_version<="3.5"',
              'pylint==2.5.2',
              'pytest~=5.4',
              'pytest-cov',
              'ipython<6',
              'twine',
              'prospector',
              'yapf',
          ],
          "docs": [
              "Sphinx==1.8.4",
              "Pygments==2.3.1",
              "docutils==0.14",
          ],
      },
      packages=['pytray'],
      test_suite='test')
