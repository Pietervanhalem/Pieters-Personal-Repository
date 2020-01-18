import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
#with open(os.path.join(here, 'README.txt')) as f:
#    README = f.read()
#with open(os.path.join(here, 'CHANGES.txt')) as f:
#    CHANGES = f.read()

requires = [
    'plaster_pastedeploy',
    'pyramid >= 1.9a',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_retry',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'faker',
    'waitress',
    'psycopg2-binary',
    'gitpython',
    'pyjade',
    'deform2000',
    'pandas',
    'numpy',
    'rollbar',
    'pyramid-mod-basemodel',
    'pyramid-mod-baseview',
    'pyramid-mod-huisstijl',
    'pyramid-mod-accounts',
    'pyramid-mod-dataframe',
    'pyramid-mod-email',
    'pyramid-mod-syncdb',
    'pyramid-mod-geommodel',
    'py-oedm-utils',
    
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
    'faker',
]

setup(
    name='sql test',
    version='0.0',
    description='',
    long_description='', #README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Author',
    author_email='author@vanoord.com',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = sql_test:main',
        ],
        'console_scripts': [
            'sql_test_initialize_db = sql_test.scripts.initializedb:main',
            'sql_test_generate_fake_data = sql_test.scripts.generate_fake_data:main',
            'sql_test_sync_db = sql_test.scripts.syncdb:main',
        ],
    },
)
