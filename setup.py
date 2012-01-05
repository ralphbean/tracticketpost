from setuptools import setup, find_packages
import sys, os

version = '0.2a6'

setup(name='tracticketpost',
      version=version,
      description="Submit new tickets to trac (via HTTP post)",
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Framework :: Trac',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='',
      author='Ralph Bean',
      author_email='ralph.bean@gmail.com',
      url='http://github.com/ralphbean/tracticketpost',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'twill',
          'BeautifulSoup',
      ],
      )
