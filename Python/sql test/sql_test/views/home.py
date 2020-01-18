"""Home page."""
from pyramid.response import Response
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError

from . import View
from pyramid_mod_accounts.models import User


class Home(View):
    """Home page container."""

    @view_config(route_name='home',
                 permission=NO_PERMISSION_REQUIRED,
                 renderer='../templates/home.jade')
    def home(self):
        """Home page."""
        try:
            self.request.session.query(User).first()
        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)

        return {}
        

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "sql_test_initialize_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
