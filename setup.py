import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'PasteScript',
    'pyramid',
    'repoze.zodbconn',
    'ZODB3',
    ]

setup(name='eye',
      version='1.0b1',
      description='A generic web-based browser of ZODB databases.',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Framework :: Pylons",
        "Framework :: ZODB",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='David Glick',
      author_email='dglick@gmail.com',
      url='http://github.com/davisagli/eye',
      keywords='zodb pyramid zope inspector',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require= requires,
      test_suite="eye",
      entry_points = """\
      [paste.app_factory]
      main = eye:eye
      [console_scripts]
      eye = eye:eye
      """,
      paster_plugins=['pyramid'],
      )
