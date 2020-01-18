"""Return a Pyramid WSGI application."""
import pkg_resources
from pyramid.config import Configurator
from pyramid.settings import asbool

__version__ = pkg_resources.get_distribution(__name__).version


def get_config(settings={}):
    """Return the app configuration."""
    
    config = Configurator(settings=settings)

    config.include("pyjade.ext.pyramid")
    config.include("pyramid_mod_basemodel")
    config.include("pyramid_mod_huisstijl")
    config.include("pyramid_mod_accounts")
    config.include("pyramid_mod_dataframe")

    config.include(".routes")

    config.scan()
    return config


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    config = get_config(settings=settings)

    return config.make_wsgi_app()
