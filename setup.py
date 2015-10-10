from setuptools import setup, find_packages
import song2

setup(
  name = song2.__song2__,
  version = song2.__version__,
  packages = find_packages(
    '.',
    exclude = [
      '*.tests', '*.tests.*', 'tests.*', 'tests',
    ]
  ),
  package_dir = {
      '' : '.'
  },
  author = song2.__author__,
  author_email = 'chemtrails.t@gmail.com',
  maintainer = 'Takumakanari',
  maintainer_email = 'chemtrails.t@gmail.com',
  description = song2.__description__,
  classifiers = [
    'Development Status :: 4 - Beta'
    'Intended Audience :: Developers',
    'License :: Other/Proprietary License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],
  install_requires = [],
  license = 'MIT',
  keywords = 'schema dict immutable typesafe',
  zip_safe = False,
  include_package_data = True
)
