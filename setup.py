import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid==1.9.2',
    'pyramid_jinja2==2.7',
    'pyramid_debugtoolbar==4.4',
    'pyramid_tm==2.2',
    'SQLAlchemy==1.2.8',
    'transaction==2.2.1',
    'zope.sqlalchemy==1.0',
    'waitress==1.1.0',
    'requests==2.19.1',
    ]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest==3.6.1',  # includes virtualenv
    ]

setup(name='geru_challenge',
      version='0.0',
      description='geru_challenge',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = geru_challenge:main
      [console_scripts]
      initialize_geru_challenge_db = geru_challenge.scripts.initializedb:main
      """,
      )
