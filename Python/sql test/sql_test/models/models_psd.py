"""Implements a PSD model."""

from urllib.parse import parse_qsl

import pandas as pd
from sqlalchemy.orm import column_property

from py_oedm_utils import dateparser

from .models import Entity, SourceFile


class PsdFile(SourceFile):
    """File that contains data of multiple psd files."""

    __mapper_args__ = {
        'polymorphic_identity': 'psd_file'
    }

    def parse(self):
        """Parse a psd file."""
        props = dict(parse_qsl(
            self.name.replace(',', '&').replace('.csv', '').split((' '))[1]))

        df = pd.read_csv(self.path)
        for i, row in df.iterrows():
            attr = {**props, **row}
            psd = Psd(source_file=self, attributes=attr)
            psd.name = attr['name.1']
            psd._date = dateparser(attr['date'])
            psd.set_xyz(
                float(attr['longitude']),
                float(attr['latitude']),
                0
            )


class Psd(Entity):
    """Table that contains the content of the datafiles."""

    __mapper_args__ = {
        'polymorphic_identity': 'psd'
    }

    attr = Entity.attributes

    density = column_property(
        attr['density'],
        deferred=False,
        info={'displayname': 'Density',
              'units': '\u03C1',
              'format': '{0:0f}'})

    quality = column_property(
        attr['quality'],
        deferred=False,
        info={'displayname': 'Quality',
              'units': '',
              'format': '{}'})
