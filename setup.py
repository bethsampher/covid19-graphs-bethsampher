"""build script used by pip
See https://packaging.python.org/tutorials/packaging-projects/
for a good intrdouction
"""
from setuptools import setup

setup(name='covid19_graphs',
      version='0.0.2',
      description='tool to download and process COVID-19 data',
      url='',
      author='Beth Sampher',
      author_email='beth.sampher@student.anglia.ac.uk',
      license='Apache 2.0',
      packages=['covid19_graphs'],
      scripts=['bin/covid19_graphs'],
      zip_safe=False,
      include_package_data=True,
      install_requires=['pytest', 'requests', 'mock', 'pandas', 'pycountry_convert'],
      python_requires='>=3.6',
      )
