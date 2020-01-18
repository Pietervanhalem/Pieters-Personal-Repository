"""Set up testing as in this example.
http://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki2/tests.html"""  # noqa
import logging
import subprocess
import os
import unittest
from pathlib import Path

import transaction
from paste.deploy.loadwsgi import appconfig

import webtest
from sql_test.models.meta import Base


log = logging.getLogger(__name__)


class FunctionalTests(unittest.TestCase):
    INI_FILE = os.path.join(os.path.dirname(__file__), 'testing.ini')
    SETTINGS = appconfig('config:' + INI_FILE)

    @classmethod
    def setUpClass(cls):

        from sql_test.models import get_tm_session
        from sql_test import main

        app = main({}, **cls.SETTINGS)
        cls.testapp = webtest.TestApp(app)

        session_factory = app.registry['session_factory']
        cls.engine = session_factory.kw['bind']
        cls.session = get_tm_session(session_factory, transaction.manager)

        Base.metadata.drop_all(bind=cls.engine)

        # run initializedb script
        args = ['sql_test_initialize_db', cls.INI_FILE]
        log.warning(subprocess.check_output(args))

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=cls.engine)
        cls.session.close()

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>sql test</h1>',
                      res.body)

class FunctionalTestsWithFauxeData(FunctionalTests):

    TEST_DATA_DIR = Path('faux_data')

    @classmethod
    def setUpClass(cls):
        from sql_test.models import CptFile, PsdFile
        from faker import Faker
        super().setUpClass()
        fake = Faker()
        fake.seed(0)

        # create faux data
        cls.nr_of_cpts = 20
        cls.nr_of_psd_files = 30

        args = ['sql_test_generate_fake_data',
                str(cls.TEST_DATA_DIR),
                str(cls.nr_of_cpts),
                str(cls.nr_of_psd_files)]
        log.warning(subprocess.check_output(args))

        # run syncdb script
        args = ['sql_test_sync_db',
                cls.INI_FILE,
                'datadirectory=' + str(cls.TEST_DATA_DIR)]
        log.warning(subprocess.check_output(args))

    @classmethod
    def tearDownClass(cls):
        import shutil
        super().tearDownClass()
        shutil.rmtree(str(cls.TEST_DATA_DIR))

    def test_nr_of_cpts(self):
        from sqlalchemy import func
        from sql_test.models import Cpt
        self.assertEqual(
            self.session.query(Cpt).count(),
            self.nr_of_cpts)

    def test_nr_of_psds(self):
        from sqlalchemy import func
        from sql_test.models import Psd, PsdFile
        self.assertEqual(
            self.session.query(PsdFile).count(),
            self.nr_of_psd_files)

        self.assertEqual(
            self.session.query(Psd).count(),
            self.nr_of_psd_files * 20)

    def test_get_a_cpt(self):
        from sqlalchemy import func
        from sql_test.models import Cpt
        cpt = self.session.query(Cpt).first()
        self.assertEqual(len(cpt.data_as_df()), 150)
        self.assertIn('name=CPT-', cpt.__repr__())