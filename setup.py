import os
import sys


try:
    from setuptools import setup
except ImportError:
    import warnings
    warnings.warn('No setuptools. Script creation will be skipped.')
    from distutils.core import setup


setup(name='ldapmigrate',
      version='0.0.1',
      description='LDAP Migrate',
      maintainer='Henry Graham',
      maintainer_email='hgraham@redhat.com',
      license='GPLv3+',
      package_dir={ 'ldapmigrate': 'ldapmigrate' },
      packages=[
          'ldapmigrate',
      ],
      scripts=[
          'bin/ldapmigrate'
      ]
)
