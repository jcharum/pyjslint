from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='pyjslint',
      version=version,
      description="Python wrapper for JSLint and Spidermonkey",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Brian Beach',
      author_email='coder@beachfamily.net',
      url='http://www.beachfamily.net/pyjslint',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      package_data={'':['*.js']},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [console_scripts]
      jslint = pyjslint:main
      """,
      )
