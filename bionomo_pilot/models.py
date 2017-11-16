from collections import OrderedDict
from sqlalchemy import Column, Integer, String
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy.ext.hybrid import hybrid_property

from bionomo_pilot.hack import gettext
from . import Components
from constants import Constants as c
from service.helper import multimedia_to_image

db = Components.db
# todo: replace this with the sql-alchemy equivalent


class Provider(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), index=True)
    abbreviation = Column(String(10), index=True)
    address = Column(String(300))
    technical_contact_name = Column(String(100))
    technical_contact_email = Column(String(100))
    technical_contact_phone = Column(String(100))
    latitude = Column(String(30))
    longitude = Column(String(30))
    nr_collections = Column(Integer)
    collection_list = db.relationship('Collection', back_populates='provider', order_by='desc(Collection.views)', lazy='dynamic')
    multimedia_list = db.relationship('Multimedia', back_populates='provider')

    @hybrid_property
    def logo(self):
        if self.multimedia_list:
            for multimedia in self.multimedia_list:
                if multimedia.type == c.CODE_IMG_LOGO:
                    return multimedia_to_image(multimedia)

    @hybrid_property
    def thumbnail(self):
        if self.multimedia_list:
            for multimedia in self.multimedia_list:
                if multimedia.type == c.CODE_IMG_THUMBNAIL:
                    return multimedia_to_image(multimedia)

    @hybrid_property
    def full_name(self):
        return self.abbreviation + " - " + self.name


class Collection(db.Model):
    id = Column(Integer, primary_key=True)
    unit_id = Column(String(100))
    unit_id_numeric = Column(Integer)
    # relationship with Provider. backref 'provider'
    provider_id = Column(Integer, db.ForeignKey('provider.id'))  # db.relationship('provider.id')
    provider = db.relationship('Provider', back_populates='collection_list')

    thumbnail_id = Column(Integer, db.ForeignKey('multimedia.id'))
    thumbnail = db.relationship('Multimedia', back_populates='collections_with_thumbnail', foreign_keys=[thumbnail_id])

    full_scientific_name = Column(String(100), index=True)
    genus = Column(String(100))
    species = Column(String(100))
    # aquisition_person = Column(String(100))
    province = Column(String(100), index=True)
    uncertainty = Column(Integer)
    district = Column(String(100))
    locality = Column(String(100))
    municipality = Column(String(100))
    authorship = Column(String(100))
    taxonomy = Column(String(300))
    identification_person = Column(String(100))
    first_date = Column(Date, index=True)
    first_year = Column(Integer, index=True)
    last_date = Column(Date, index=True)
    last_year = Column(Integer, index=True)
    location = Column(String(300))
    latitude = Column(Float(30), index=True)
    longitude = Column(Float(30), index=True)
    views = Column(Integer, default=0)
    multimedia_list = db.relationship('Multimedia', back_populates='collection',
                                      order_by='asc(Multimedia.order)', lazy='dynamic',
                                      foreign_keys="Multimedia.collection_id")

    @hybrid_property
    def thumbnail_img(self):
        if self.thumbnail:
            return multimedia_to_image(self.thumbnail)

    @hybrid_property
    def thumbnail_big(self):
        if self.multimedia_list.count() > 0:
            for multimedia in self.multimedia_list:
                if multimedia.type == c.CODE_IMG_THUMBNAIL:
                    return multimedia_to_image(multimedia)
        else:
            if self.provider and self.provider.thumbnail:
                return self.provider.thumbnail

    @hybrid_property
    def as_dict(self):
        return OrderedDict([
            (gettext('header.unit_id'), self.unit_id if self.unit_id else ''),
            (gettext('header.scientific_name'), self.full_scientific_name if self.full_scientific_name else ''),
            (gettext('header.authorship'), self.authorship if self.authorship else ''),
            (gettext('header.genus'), self.genus if self.genus else ''),
            (gettext('header.species'), self.species if self.species else ''),
            (gettext('header.taxonomy'), self.taxonomy if self.taxonomy else ''),
            (gettext('header.authorship'), self.authorship if self.authorship else ''),
            (gettext('header.province'), self.province if self.province else ''),
            (gettext('header.district'), self.district if self.district else ''),
            (gettext('header.longitude'), self.longitude if self.longitude else ''),
            (gettext('header.latitude'), self.latitude if self.latitude else ''),
            (gettext('header.provider'), self.provider.full_name if self.provider.full_name else ''),
            (gettext('header.last_date'), self.last_date.strftime(c.general_date_format) if self.last_date else ''),
        ])
    @hybrid_property
    def taxonomy_dict(self):
        _dict = None

        if self.taxonomy:
            _dict = OrderedDict()
            input_parts = self.taxonomy.split('[')
            input_parts = [input_part for input_part in input_parts if len(input_part) > 1]

            for part in input_parts:
                inner_parts = part.split(']')
                key = inner_parts[0]
                value = inner_parts[1][2:]
                _dict[key] = value

        return _dict

class Multimedia(db.Model):
    id = Column(Integer, primary_key=True)
    short_name = Column(String(50))
    full_name = Column(String(50))
    description = Column(String(100))
    type = Column(Integer, index=True)    # will be mapped on 'constants' all the types: 1-images, 2-documents, 3-other
    order = Column(Integer)    # order of presentation of the multimedia. for images the first will be displayed as
    # relationship with Collection. backref 'collection'
    collection_id = Column(Integer, db.ForeignKey('collection.id'))
    collection = db.relationship('Collection', back_populates='multimedia_list', foreign_keys=[collection_id])
    collections_with_thumbnail = db.relationship('Collection', back_populates='thumbnail',
                                                 foreign_keys="Collection.thumbnail_id")
    # relationship with Provider. backref 'provider'
    provider_id = Column(Integer, db.ForeignKey('provider.id'))     # images are exclusive to provider (building, etc) when collection_id is null
    provider = db.relationship('Provider', back_populates='multimedia_list')
