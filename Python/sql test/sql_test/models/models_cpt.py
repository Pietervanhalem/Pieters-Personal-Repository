"""Implements a cpt model."""

from urllib.parse import parse_qsl

import pandas as pd

from .models import Entity, SourceFile
from py_oedm_utils import dateparser


class CptFile(SourceFile):
    """File that contains data of one cpt."""

    __mapper_args__ = {
        'polymorphic_identity': 'cpt_file'
    }

    def parse(self):
        """Parse a cpt file."""
        props = dict(parse_qsl(
            self.name.replace(',', '&').replace('.csv', '').split((' '))[1]))

        cpt = Cpt(source_file=self, attributes=props)
        cpt._date = dateparser(props['date'])
        cpt.name = props['name']
        cpt.set_xyz(
            float(props['longitude']),
            float(props['latitude']),
            0
        )

        df = pd.read_csv(self.path)
        cpt.data_to_df(df)


class Cpt(Entity):
    """Table that contains the content of the datafiles."""

    __mapper_args__ = {
        'polymorphic_identity': 'cpt'
    }
