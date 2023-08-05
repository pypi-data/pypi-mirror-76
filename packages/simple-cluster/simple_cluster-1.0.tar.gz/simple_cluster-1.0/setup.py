# TODO: Fill out this file with information about your package

# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/
from setuptools import setup

setup(name='simple_cluster',
      version='1.0',
      description='A simply realisation of k-means and k-means++',
      packages=['simple_cluster'],
      author = 'Lujing Yang',
      author_email = 'lujing@me.com',
      zip_safe=False)

