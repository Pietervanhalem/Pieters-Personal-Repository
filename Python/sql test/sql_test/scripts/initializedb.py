"""Use this script to initilize the database.
This script will create the required database model
"""
import os
import sys

import transaction
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars

from pyramid_mod_accounts.models import Role, User, UserRole

from .. import get_config
from ..models import get_engine, get_session_factory, get_tm_session
from ..models.meta import Base


def usage(argv):
    """Give feedback on commandline usage."""
    cmd = os.path.basename(argv[0])
    print(
        "usage: %s <config_uri> [var=value]\n"
        '(example: "%s development.ini")' % (cmd, cmd)
    )
    sys.exit(1)


def main(argv=sys.argv):
    """Initiliaze database.
    Standard database roles and an admin user is added to the database.
    """
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings = get_config(settings=settings).get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)
    session_factory = get_session_factory(engine)

    role_names = ["authorised", "admin"]
    with transaction.manager:
        session = get_tm_session(session_factory, transaction.manager)
        user = session.query(User).limit(1).one_or_none()
        if not user:
            user = User(name="admin", email="admin@example.com")
            user.password = "admin"
            session.add(user)
            session.flush()
            session.refresh(user)
            for role_name in role_names:
                role = Role()
                role.name = role_name
                role.created_by_user_id = user.id
                session.add(role)
                session.flush()
                session.refresh(role)
                userrole = UserRole()
                userrole.role_id = role.id
                userrole.user_id = user.id
                userrole.created_by_user_id = user.id
                session.add(userrole)

    print("Database model created!")