"""build script used by pip
See https://packaging.python.org/tutorials/packaging-projects/
for a good intrdouction
"""
from setuptools import setup

setup(name='covid19_graphs',
      version='0.0.1',
      description='tool to download and process COVID-19 data',
      url='',
      author='Oliver Smart',
      author_email='oliver.smart@anglia.ac.uk',
      license='Apache 2.0',
      packages=['covid19_graphs'],
      scripts=['bin/covid19_graphs'],
      zip_safe=False,
      include_package_data=True,
      install_requires=['pytest', 'requests'],
      python_requires='>=3.6',
      )
