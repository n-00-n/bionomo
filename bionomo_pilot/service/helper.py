import base64
from bionomo_pilot.config import Config as cfg


class Coordinate(object):
    def __init__(self, latitude=None, longitude=None, data_provider_name=None, species=None):
        self.latitude = latitude
        self.longitude = longitude
        self.data_provider_name = data_provider_name
        self.species = species


class Image(object):
    def __init__(self, multimedia_id=None, name=None, description=None, url=None, width=None, height=None):
        self.multimedia_id = multimedia_id
        self.name = name
        self.description = description
        self.url = url
        self.width = width
        self.height = height


def encode_text(text):
    return base64.b64encode(text)


def decode_text(text):
    return base64.b64decode(text)


def multimedia_to_image(multimedia, width=None, height=None):
    _encoded_multimedia_id = encode_text(str(multimedia.id)) if multimedia is not None else encode_text('-1')
    _encoded_multimedia_type = encode_text(str(multimedia.type)) if multimedia is not None else ''

    _url = '/'.join([cfg.MULTIMEDIA_ENDPOINT,
                     _encoded_multimedia_id,
                     _encoded_multimedia_type])

    return Image(multimedia_id=multimedia.id,
                 name=multimedia.short_name,
                 description=multimedia.description,
                 url=_url,
                 width=width,
                 height=height)


def get_general_date_as_string(date):
    return ''


def collection_to_csv(collection_list):
    pass


