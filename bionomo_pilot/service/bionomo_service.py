from collections import OrderedDict

import io

import unicodecsv as csv
from sqlalchemy import asc
from sqlalchemy import desc

from bionomo_pilot import Components
from bionomo_pilot.models import Provider, Collection
from bionomo_pilot.models import Multimedia
from helper import multimedia_to_image
from bionomo_pilot.constants import Constants as c
from bionomo_pilot.biocase.constants import Constants as b_c

db = Components.db


class BioNoMoService(object):
    def __init__(self):
        self.provinces = None

    def get_portal_data(self):

        providers = self.get_partner_stats()
        stakeholders = self.get_stacke_holders_images()
        stakeholders_big = self.get_stacke_holders_big_images()
        portal_images = self.get_portal_images()

        _data_dict = {
            'partner_stats': providers,
            'providers': providers,
            'stakeholders': stakeholders,
            'stakeholders_big': stakeholders_big,
            'images': portal_images,
        }

        return _data_dict

    def get_image(self, short_name, image_type, height=None):
        multimedia = Multimedia.query.filter(Multimedia.short_name == short_name, Multimedia.type == image_type).one()
        return multimedia_to_image(multimedia, height=height)

    def load_multimedia_by_id(self, multimedia_id):
        return Multimedia.query.get(multimedia_id)

    def get_partner_stats(self):
        return self.get_providers()

    def get_stacke_holders_images(self):
        _images_list = [
            ('logo_url_uem', self.get_image('logo_uem', c.CODE_IMG_LOGO, height=80)),
            ('logo_url_sapienza', self.get_image('logo_unisapienzia', c.CODE_IMG_LOGO, height=70)),
            ('logo_url_museu', self.get_image('logo_museu', c.CODE_IMG_LOGO)),
            ('logo_url_iiam', self.get_image('logo_iiam', c.CODE_IMG_LOGO)),
            ('logo_url_cbt', self.get_image('logo_cbt', c.CODE_IMG_LOGO)),
            ('logo_url_uem_biology', self.get_image('logo_uem_biology', c.CODE_IMG_LOGO, height=70)),
        ]

        return OrderedDict(_images_list)

    def get_stacke_holders_big_images(self):
        _images_list = [
            ('logo_url_mitader', self.get_image('logo_mitader', c.CODE_IMG_LOGO)),
        ]

        return OrderedDict(_images_list)

    def get_portal_images(self):
        _images_list = {
            'logo_url_main': self.get_image('logo_bionomo', c.CODE_IMG_LOGO),
            'logo_url_uem': self.get_image('logo_uem', c.CODE_IMG_LOGO),
            'logo_url_sapienza': self.get_image('logo_unisapienzia', c.CODE_IMG_LOGO),
            'logo_url_aics': self.get_image('logo_aics', c.CODE_IMG_LOGO),
            'logo_url_museu': self.get_image('logo_museu', c.CODE_IMG_LOGO),
            # 'logo_url_iiam': self.get_image('logo_iiam', c.CODE_IMG_LOGO),
            'thumb_url_museu': self.get_image('thumb_museu', c.CODE_IMG_THUMBNAIL),
            # 'thumb_url_iiam': self.get_image('thumb_iiam', c.CODE_IMG_THUMBNAIL),
            'flag_url_pt': self.get_image('flag_pt', c.CODE_IMG_FLAG),
            'flag_url_uk': self.get_image('flag_uk', c.CODE_IMG_FLAG),
            'flag_url_it': self.get_image('flag_it', c.CODE_IMG_FLAG),
            'flag_url_fr': self.get_image('flag_fr', c.CODE_IMG_FLAG),
        }

        return _images_list

    def get_providers(self):
        return Provider.query.all()

    def get_collections_by_scientific_name_with_limit(self, scientific_name, limit=None):
        collection_filter = Collection.query.filter(Collection.full_scientific_name.like('%' + scientific_name + '%')) \
                                            .distinct(Collection.full_scientific_name).group_by(Collection.full_scientific_name)\
                                            .limit(limit if limit else 5)

        return collection_filter

    def get_collections_by_scientific_name(self, scientific_name, page=None):
        """get's the scientific name

        :returns dict {
                        'collections': collection_to_query;
                        'data_providers': data_providers_to_query;
                        'provinces': provinces_to_query;
                       }
        """
        return self.get_collections_by_fields(scientific_name=scientific_name, is_simple_search=True)

    def get_collections_by_fields(self, scientific_name=None, province_list=None, provider_id_list=None, latitude=None,
                                  longitude=None, start_date=None, end_date=None, page=None, items_per_page=None,
                                  start_latitude=None, end_latitude=None, start_longitude=None, end_longitude=None, is_simple_search=False):

        collection_filter = Collection.query.filter(Collection.full_scientific_name.like('%' + scientific_name + '%'),
                                                    Collection.province.in_(province_list) if province_list else True,
                                                    Collection.provider_id.in_(provider_id_list) if provider_id_list else True,
                                                    Collection.latitude >= start_latitude if start_latitude else True,
                                                    Collection.latitude <= end_latitude if end_latitude else True,
                                                    Collection.longitude >= start_longitude if start_longitude else True,
                                                    Collection.longitude <= end_longitude if end_longitude else True,
                                                    Collection.last_date >= start_date if start_date else True,
                                                    Collection.last_date <= end_date if end_date else True)

        collection_list = collection_filter.paginate(page=(page if page else 1),
                                                     per_page=(items_per_page if items_per_page else c.collections_per_page),
                                                     error_out=False)

        # don't bother continue since we don't have data on the list
        if collection_list.total == 0:
            return None

        collection_distinct_providers = collection_filter.distinct(Collection.provider_id).group_by(Collection.provider_id)
        providers = [collection.provider for collection in collection_distinct_providers]

        collection_distinct_provinces = collection_filter.distinct(Collection.province).group_by(Collection.province)
        provinces = [collection.province for collection in collection_distinct_provinces if collection.province is not None]

        collections_coordinates = collection_filter.limit(c.gmaps_markers_limit)

        min_latitude_filter = collection_filter.order_by(asc(Collection.latitude)).limit(1)
        max_latitude_filter = collection_filter.order_by(desc(Collection.latitude)).limit(1)
        min_max_latitude = [min_latitude_filter, max_latitude_filter]
        _min_latitude = min_max_latitude[0][0].latitude if min_max_latitude[0][0] else ''
        _max_latitude = min_max_latitude[1][0].latitude if min_max_latitude[1][0] else ''

        min_longitude_filter = collection_filter.order_by(asc(Collection.longitude)).limit(1)
        max_longitude_filter = collection_filter.order_by(desc(Collection.longitude)).limit(1)
        min_max_longitude = [min_longitude_filter, max_longitude_filter]
        _min_longitude = min_max_longitude[0][0].longitude if min_max_longitude[0][0] else ''
        _max_longitude = min_max_longitude[1][0].longitude if min_max_longitude[1][0] else ''

        _result = {
            'collections': collection_list,
            'collections_coordinates': collections_coordinates,
            'data_providers': providers,
            'provinces': provinces,
            'simple_form_values': {
                b_c.name_full_scientific_name_string: scientific_name
            } if is_simple_search else None,

            'advanced_form_values': {
                    b_c.name_full_scientific_name_string: scientific_name
                } if is_simple_search else
                {
                    b_c.name_full_scientific_name_string: scientific_name,
                    b_c.name_province: province_list,
                    b_c.name_latitude_decimal_start: start_latitude,
                    b_c.name_latitude_decimal_end: end_latitude,
                    b_c.name_longitude_decimal_start: start_longitude,
                    b_c.name_longitude_decimal_end: end_longitude,
                    b_c.name_last_date_start: start_date.strftime(c.date_format) if start_date else None,
                    b_c.name_last_date_end: end_date.strftime(c.date_format) if end_date else None,
                },

            'filter_form_values': {
                'data_providers': providers,
                b_c.name_full_scientific_name_string: scientific_name,
                b_c.name_province: province_list,
                b_c.name_latitude_decimal_start: _min_latitude,
                b_c.name_latitude_decimal_end: _max_latitude,
                b_c.name_longitude_decimal_start: _min_longitude,
                b_c.name_longitude_decimal_end: _max_longitude,
                b_c.name_last_date_start: start_date.strftime(c.date_format) if start_date else None,
                b_c.name_last_date_end: end_date.strftime(c.date_format) if end_date else None,
            }
        }

        return _result

    def get_csv_for_fields(self, scientific_name=None, province_list=None, provider_id_list=None, latitude=None,
                                  longitude=None, start_date=None, end_date=None, page=None, items_per_page=None,
                                  start_latitude=None, end_latitude=None, start_longitude=None, end_longitude=None, is_simple_search=False):

        collection_filter = Collection.query.filter(Collection.full_scientific_name.like('%' + scientific_name + '%'),
                                                    Collection.province.in_(province_list) if province_list else True,
                                                    Collection.provider_id.in_(provider_id_list) if provider_id_list else True,
                                                    Collection.latitude >= start_latitude if start_latitude else True,
                                                    Collection.latitude <= end_latitude if end_latitude else True,
                                                    Collection.longitude >= start_longitude if start_longitude else True,
                                                    Collection.longitude <= end_longitude if end_longitude else True,
                                                    Collection.last_date >= start_date if start_date else True,
                                                    Collection.last_date <= end_date if end_date else True)

        if collection_filter.count() == 0:
            return None

        output = io.BytesIO()
        with open('test.csv', 'w') as file:
            w = csv.DictWriter(file, fieldnames=collection_filter[0].as_dict.keys())
            w.writeheader()
            w.writerows([collection.as_dict for collection in collection_filter])

        w = csv.DictWriter(output, fieldnames=collection_filter[0].as_dict.keys())
        w.writeheader()
        w.writerows([collection.as_dict for collection in collection_filter])

        # output.close()

        return output

    def get_provinces(self):
        # for efficiency
        if not self.provinces:
            self.provinces = provinces = ['Maputo', 'Gaza', 'Inhambane', 'Sofala', 'Manica', 'Tete', 'Quelimane', 'Nampula', 'Niassa', 'Cabo Delgado']
        return self.provinces

    def is_valid_province_list(self, province_list):
        return len(province_list) == Collection.query.filter(Collection.province.in_(province_list)).distinct(Collection.province).group_by(Collection.province).count()

    def is_valid_provider_id_list(self, id_list):
        return len(id_list) == Provider.query.filter(Provider.id.in_(id_list)).count()

    def get_providers_with_ids(self, id_list):
        return Provider.query.filter(Provider.id.in_(id_list))

    def gen_csv(self, collection_list_gen):
        output = io.StringIO()
        w = csv.DictWriter(output, encoding='utf-8', fieldnames=collection_list_gen[0].as_dict.keys())
        w.writeheader()
        w.writerows(collection_list_gen)

        return output

