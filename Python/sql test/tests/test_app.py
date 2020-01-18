import logging
import os
import unittest
from urllib.parse import urljoin, urlparse

import pytest
import transaction
from paste.deploy.loadwsgi import appconfig
from pyramid import testing
from sqlalchemy import DDL, event

log = logging.getLogger(__name__)


def find_urls(res):
    """Find all urls."""
    urls = []
    for tag in res.html.findAll('', src=True):
        if not tag['src'].startswith('#'):
            urls.append(urljoin(res.request.url, tag['src']))

    for tag in res.html.findAll('', href=True):
        if not tag['href'].startswith('#'):
            urls.append(urljoin(res.request.url, tag['href']))
    return urls


def visit_local_urls(res, urls):
    """Visit urls."""
    for url in urls:
        if 'sign_out' in url:
            continue
        if urlparse(url).netloc == urlparse(res.request.url).netloc:
            print(url, end='')
            res.test_app.get(url, status=200)
            print('  ...ok')


def find_and_visit_local_urls(res):
    """Find and test availablility of all urls."""
    urls = find_urls(res)
    visit_local_urls(res, urls)


def dummy_request(session):
    return testing.DummyRequest(session=session)


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = testing.setUp(settings={})
        cls.config.include('pyramid_mod_basemodel')
        settings = cls.config.get_settings()

        from sql_test.models.meta import Base
        from sql_test.models import (
            get_engine,
            get_session_factory,
            get_tm_session,
        )

        cls.engine = get_engine(settings)
        session_factory = get_session_factory(cls.engine)
        cls.session = get_tm_session(session_factory, transaction.manager)
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        from sql_test.models.meta import Base
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(cls.engine)
        cls.session.close()


class TestDatabase(BaseTest):

    def test_version(self):
        from sqlalchemy import func
        import re
        v = self.session.query(func.version()).one()[0]
        self.assertRegex(v, r'PostgreSQL 1\d\.\d+')

class TestPostgis(BaseTest):

    @classmethod
    def setUpClass(cls):
        import pyramid_mod_geommodel
        super().setUpClass()
    
    def test_postgis_version(self):
        from sqlalchemy import func
        import re
        v = self.session.query(func.PostGIS_full_version()).one()[0]
        self.assertRegex(v, r'POSTGIS="2\.')

    def test_postgis_transformation(self):
        from sqlalchemy import func
        v = self.session.query(func.ST_AsText(
            func.ST_Transform(
                func.ST_GeomFromText(
                    ('POLYGON(('
                     '743238 2967416,'
                     '743238 2967450,'
                     '743265 2967450,'
                     '743265.625 2967416,'
                     '743238 2967416))'),
                    2249), 4326))).one()[0]
        self.assertEqual(v, (
            'POLYGON(('
            '-71.1776848522251 42.3902896512902,'
            '-71.1776843766326 42.3903829478009,'
            '-71.1775844305465 42.3903826677917,'
            '-71.1775825927231 42.3902893647987,'
            '-71.1776848522251 42.3902896512902))'
        ))

class FunctionalTests(BaseTest):
    INI_FILE = os.path.join(os.path.dirname(__file__), 'testing.ini')
    SETTINGS = appconfig('config:' + INI_FILE)

    @classmethod
    def setUpClass(cls):
        super(FunctionalTests, cls).setUpClass()

        # run initializedb script
        stmnt = ' '.join(['sql_test_initialize_db',
                          cls.INI_FILE])
        log.warning(stmnt)
        os.system(stmnt)

        # start demo app
        from sql_test import main
        app = main({}, **cls.SETTINGS)
        from webtest import TestApp
        cls.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>sql test</h1>',
                      res.body)

    def test_home_urls(self):
        res = self.testapp.get('/', status=200)
        find_and_visit_local_urls(res)
    def test_jade(self):
        res = self.testapp.get('/jade_demo', status=200)
        self.assertIn(b'jade',
                      res.body)

    def test_jade_urls(self):
        res = self.testapp.get('/jade_demo', status=200)
        find_and_visit_local_urls(res)

    def test_huisstijl(self):
        res = self.testapp.get('/bootstrap_demo', status=200)
        self.assertIn(b'Cras mattis consectetur purus sit amet fermentum.',
                      res.body)

    def test_huisstijl_urls(self):
        res = self.testapp.get('/bootstrap_demo', status=200)
        find_and_visit_local_urls(res)

class FunctionalTestsAdmin(BaseTest):
    INI_FILE = os.path.join(os.path.dirname(__file__), 'testing.ini')
    SETTINGS = appconfig('config:' + INI_FILE)

    @classmethod
    def setUpClass(cls):
        """Sign in."""
        super(FunctionalTestsAdmin, cls).setUpClass()

        # run initializedb script
        stmnt = ' '.join(['henky_initialize_db',
                          cls.INI_FILE])
        log.warning(stmnt)
        os.system(stmnt)

        # start demo app
        from henky import main
        app = main({}, **cls.SETTINGS)
        from webtest import TestApp
        cls.testapp = TestApp(app)

        res = cls.testapp.get("/sign_in_local", status=200)
        f = res.forms["sign-in"]
        f.set("user_name", "admin")
        f.set("password", "admin")
        res = f.submit("submit")

    def tearDown(self):
        """Sign out."""
        self.testapp.get("/sign_out")

    def test_home_urls(self):
        """Test urls from home."""
        res = self.testapp.get("/", status=200)
        self.assertEqual(200, res.status_code)
        #find_and_visit_local_urls(res)