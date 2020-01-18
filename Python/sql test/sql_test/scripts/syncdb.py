"""Use this script to sync files to the database."""
import os
import sys
from pathlib import Path

import transaction
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars

from pyramid_mod_syncdb.utils import sync_files_to_db

from .. import get_config
from ..models import get_engine, get_session_factory, get_tm_session
from ..models import CptFile, PsdFile

SCRIPT = os.path.abspath(__file__)


def usage(argv):
    """Give feedback on commandline usage."""
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    """Synchronize files to database."""
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    settings.update(options)
    settings = get_config(settings=settings).get_settings()
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)

    datadirectory = settings.get('datadirectory')
    if datadirectory is None:
        raise ValueError('datadirectory not defined')
    datadirectory = Path(datadirectory)

    # Add the directories to be synchronized here.
    with transaction.manager:
        session = get_tm_session(session_factory, transaction.manager)
        paths = datadirectory.joinpath('cpt').glob('**/*.csv')
        sync_files_to_db(session, CptFile, paths, script=SCRIPT)

    with transaction.manager:
        session = get_tm_session(session_factory, transaction.manager)
        paths = datadirectory.joinpath('psd').glob('**/*.csv')
        sync_files_to_db(session, PsdFile, paths, script=SCRIPT)