from setuptools import setup
from itertools import chain
import os
import codecs
import re

python_requires = ">=3.6"
install_requires = ['numpy']
lebesgue_require = ['scipy']
tests_require = ['matplotlib', 'pytest', 'coverage']
docs_require = [
        'matplotlib',
        'sphinx',
        'sphinxcontrib-bibtex',
        'sphinxcontrib-tikz']
extras_require = {
        'test': tests_require,
        'doc': docs_require,
        'lebesgue': lebesgue_require}

extras_require['all'] = list(chain(*extras_require.values()))

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='recursivenodes',
      version=find_version('recursivenodes', '__init__.py'),
      description='Recursively defined interpolation nodes for the simplex',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Toby Isaac',
      author_email='tisaac@cc.gatech.edu',
      packages=['recursivenodes'],
      package_dir={'recursivenodes': 'recursivenodes'},
      python_requires=python_requires,
      install_requires=install_requires,
      package_data={'recursivenodes': [
          'lebesgue_constants.csv',
          'more_lebesgue_constants.csv']},
      tests_require=['matplotlib', 'pytest'],
      license='MIT',
      url="https://tisaac.gitlab.io/recursivenodes/",
      project_urls={
          "Bug Tracker": "https://gitlab.com/tisaac/recursivenodes/issues",
          "Source Code": "https://gitlab.com/tisaac/recursivenodes/",
          },
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Intended Audience :: Science/Research",
          "Natural Language :: English",
          "Topic :: Scientific/Engineering :: Mathematics",
      ],
      extras_require=extras_require,
      )
