import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '1.1'
PACKAGE_NAME = 'towercrane'
AUTHOR = 'Taha'
AUTHOR_EMAIL = 'taha.m.ashtiani@gmail.com'
URL = 'https://github.com/ashtianicode'

LICENSE = 'MIT'
DESCRIPTION = 'TowerCrane helps you keep your large local datasets in the cloud'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'fire',
      'boto3',
      'db-sqlite3',
      'zipfile36',
      'tabulate'
      
]

ENTRY ={
          'console_scripts': [
              'towercrane = towercrane.main:main',
          ],
      }

CLASSIFIERS= [
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Operating System :: MacOS',
          'Operating System :: Unix',
          'Topic :: Office/Business :: Financial :: Investment',
      ]


setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      entry_points=ENTRY,
      classifiers=CLASSIFIERS
      )