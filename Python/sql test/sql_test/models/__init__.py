"""Contains imports of all models.

import or define all models here to ensure they are attached to the
Base.metadata prior to any initialization routines
"""

from pyramid_mod_basemodel import (get_engine, get_session_factory,  # noqa
                              get_tm_session)
from sqlalchemy.orm import configure_mappers
from pyramid_mod_basemodel import metadata  # noqa
from .models import Base  # noqa

from .models_cpt import CptFile, Cpt  # noqa
from .models_psd import PsdFile, Psd  # noqa
# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()
