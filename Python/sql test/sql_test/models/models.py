"""Implements data model."""
from datetime import date

import pandas as pd
from sqlalchemy import (Column, Date,  ForeignKey, Integer, Sequence,
                        String)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship
from pyramid_mod_basemodel import Base  # noqa
from pyramid_mod_geommodel import PointMixin  # noqa
from pyramid_mod_syncdb.models import SourceFileMixin


class Entity(Base, PointMixin):
    """Table that contains the content of the datafiles.
    This is the actual table that will be part to the database.

    The entity_type attribute is used to place different kind of entities
    in the same database table with single table inheritance:
    http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#single-table-inheritance
    """

    srid_local = 4326

    __tablename__ = 'entity'
    entity_type = Column(
        String(20),
        info={'displayname': 'Entity type',
              'units': '',
              'format': '{}'})
    __mapper_args__ = {
        'polymorphic_on': entity_type,
        'polymorphic_identity': 'entity'
    }

    id = Column(
        Integer,
        Sequence('entity_id_seq'),
        primary_key=True)
    name = Column(String)
    sourcefile_id = Column(
        Integer,
        ForeignKey('source_file.id', ondelete='CASCADE'),
        nullable=False)
    attributes = Column(JSONB)
    data = Column(JSONB)
    _date = Column(
        'date',
        Date,
        info={'displayname': 'Date of testing/sampling/installation',
              'units': '',
              'format': '{:%Y-%m-%d}'})

    def __repr__(self):
        entity_type = self.__mapper_args__['polymorphic_identity'].upper()
        attr_str = ', '.join(['{}={}'.format(k, v)
                              for k, v in self.attributes.items()])
        return '<{} {}>'.format(entity_type, attr_str)

    def data_as_df(self):
        """Return data attribute as pandas dataframe."""
        return pd.DataFrame.from_dict(self.data)

    def data_to_df(self, df):
        """Set data attribute from pandas dataframe."""
        self.data = df.to_dict(orient='list')

class SourceFile(SourceFileMixin, Base):
    """Base SourceFile implementation.

    Uses single table inheritance:
    http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#single-table-inheritance
    """

    __tablename__ = 'source_file'
    id = Column(Integer,
                Sequence('source_file_id_seq'),
                primary_key=True)
    file_type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on': file_type,
        'polymorphic_identity': 'source_file'
    }

    def parse(self):
        """Parse this file (used by sync_to_db)."""
        raise NotImplementedError()

    entities = relationship(
        'Entity',
        backref=backref("source_file"),
        cascade="all,delete"
    )

    # TODO: hoort dit hier wel?
    @hybrid_property
    def date(self):
        """Date."""
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, date):
            raise ValueError('Date must be of type date')
        else:
            self._date = value