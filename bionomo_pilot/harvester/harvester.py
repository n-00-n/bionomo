from datetime import datetime
from bionomo_pilot.models import Provider, Collection, Multimedia
from ..biocase.protocol_query import ProtocolQuery
from ..biocase.constants import Constants as c
from bionomo_pilot import Components

db = Components.db


class Harvester:
    def __init__(self):
        pass

    def load_top_10(self):
        """Load top 10 from BioCase using the BioCase Protocol
        :returns collection_item_list

        Models: bionomo_pilot.biocase.models.CollectionItem"""
        protocol_query = ProtocolQuery()
        protocol_query.set_direct_text('as')
        biocase_result = protocol_query.fetch_result()

        return biocase_result.collection_items;

    def load_and_parse(self):
        """Loads top 10 from BioCase using the BioCase Protocol
        and parses it to Portal models

        :returns provider_list:

        Models: bionomo_pilot.models.Provider,
              bionomo_pilot.models.Collection
        """
        protocol_query = ProtocolQuery()
        protocol_query.set_direct_text('as')
        biocase_result = protocol_query.fetch_result()

        provider_list = []
        for abcd_model in biocase_result.abdc_models:
            provider = Provider()
            provider.name = abcd_model.provider.org_name
            provider.abbreviation = abcd_model.provider.org_abbrv
            provider.address = abcd_model.provider.address
            provider.technical_contact_name = abcd_model.provider.contact_name
            provider.technical_contact_email = abcd_model.provider.contact_email
            provider.latitude = ""
            provider.longitude = ""
            provider.nr_collections = len(abcd_model.collection_items)

            provider_list.append(provider)

        return provider_list

    def load_parse_and_submit(self):
        """Loads top 10 from BioCase using the BioCase Protocol
        parses it to Portal models and then submits it to the database

        :returns True if succeeded,
                 False if not succeeded.
        """
        protocol_query = ProtocolQuery()
        attribute_dict = {
            'path': c.full_path_unit_id,
            'operation': c.query_conjuction_op_greather_than_tag,
            'value': '29500'
        }
        protocol_query.set_attribute_dict(attribute_dict)
        biocase_result = protocol_query.fetch_result()
        none_failed = True
        provider_list = []

        for abcd_model in biocase_result.abdc_models:
            provider = Provider()
            provider.name = abcd_model.provider.org_name
            provider.abbreviation = abcd_model.provider.org_abbrv
            provider.address = abcd_model.provider.address
            provider.technical_contact_name = abcd_model.provider.contact_name
            provider.technical_contact_email = abcd_model.provider.contact_email
            provider.latitude = None    # todo: implement this.
            provider.longitude = None    # todo: implement this.
            provider.nr_collections = len(abcd_model.collection_items)  # todo: remove this, compute count once on the biocase_results.fetch_results()

            collection_list = []

            for collection_item in abcd_model.collection_items:
                collection = Collection()

                collection.unit_id = collection_item.get_attribute(c.attrs[c.name_unit_id]['name']).values[0]
                collection.full_scientific_name = collection_item.get_attribute(c.attrs[c.name_full_scientific_name_string]['name']).values[0]
                collection.authorship = collection_item.get_attribute(c.attrs[c.name_authorship]['name']).values[0]

                collection.taxonomy = collection_item.get_attribute(c.attrs[c.name_taxonomy]['name']).values[0]
                collection.genus = self.get_from_taxonomy(collection.taxonomy, '[Genus]')
                collection.species = self.get_from_taxonomy(collection.taxonomy, '[Species]')

                collection.province = collection_item.get_attribute(c.attrs[c.name_province]['name']).values[0]
                collection.district = collection_item.get_attribute(c.attrs[c.name_district]['name']).values[0]

                _date_str = collection_item.get_attribute(c.attrs[c.name_last_date]['name']).values[0]
                collection.date = datetime.strptime(_date_str, c.date_format) if _date_str else None
                collection.year = collection.date.year if collection.date else None

                _latitude_str = collection_item.get_attribute(c.attrs[c.name_latitude_decimal]['name']).values[0]
                collection.latitude = float(_latitude_str) if _latitude_str else None

                _longitude_str = collection_item.get_attribute(c.attrs[c.name_longitude_decimal]['name']).values[0]
                collection.longitude = float(_longitude_str) if _longitude_str else None

                collection_list.append(collection)

            if collection_list:
                provider.collection_list = collection_list

            try:
                db.session.add(provider)
                db.session.commit()
            except:
                none_failed = False
                raise Exception('something went wrong')

            provider_list.append(provider)

        return none_failed

    def harvest(self):
        # load abcd_models from protocol_query
        # saves it to the db
        # if it has more, loads and save it
        _harvested = 0
        protocol_query = ProtocolQuery()
        #initialize the query
        attribute_dict = {
            'path': c.full_path_unit_id,
            'operation': c.query_conjuction_op_greather_than_tag,
            'value': '0'
        }

        protocol_query.set_attribute_dict(attribute_dict)
        _count = 0
        for abcd_model in protocol_query.fetch_result_as_ABCDModels():
            _count += self._submit_to_abcd_model_to_DB(abcd_model)

            if abcd_model.has_more_items:
                _abcd_model = abcd_model
                while _abcd_model.has_more_items:
                    print('found more items on the ABCDModel.')
                    _attribute_dict = {
                        'path': c.full_path_unit_id,
                        'operation': c.query_conjuction_op_greather_than_tag,
                        'value': _abcd_model.flag
                    }

                    _abcd_model = protocol_query.load_more_from_ABCDModel(abcd_model, _attribute_dict)
                    _count += self._submit_to_abcd_model_to_DB(_abcd_model, True)

        return _count

    def _submit_to_abcd_model_to_DB(self, abcd_model, add_to_collection=False):    # add_to_collection: whether or not this should update the collection
        """Submits ABCDModel object.
        :returns the number of CollectionItems correspondents on teh model submitted"""
        # extract a provider bionomo_pilot.models
        # check if the provider model is on db: use abbreviation
        # if not: keep model, if yes: load model from the DB instead and update the collection_nrs

        provider = Provider()
        provider.name = abcd_model.provider.org_name
        provider.abbreviation = abcd_model.provider.org_abbrv
        provider.address = abcd_model.provider.address
        provider.technical_contact_name = abcd_model.provider.contact_name
        provider.technical_contact_email = abcd_model.provider.contact_email
        provider.latitude = None  # todo: implement this.
        provider.longitude = None  # todo: implement this.
        provider.nr_collections = len(abcd_model.collection_items)

        _provider_db = db.session.query(Provider).filter(Provider.name == provider.name).first()

        if not _provider_db and add_to_collection:
            raise Exception('Please call this method providing an already existing provider '
                            'or set add_to_collection=False. [{}]'.format(provider.abbreviation))
        elif not _provider_db:
            db.session.add(provider)
            db.session.commit()

        if _provider_db:
            # just update the nr_collections
            # commit to the db.
            _provider_db.nr_collections += provider.nr_collections
            db.session.commit()

            provider = _provider_db
        else:
            # save it to the DB
            db.session.add(provider)
            db.session.commit()

        # update the multimedia table
        multimedia_list = db.session.query(Multimedia).filter(Multimedia.provider_abbrv == provider.abbreviation)
        for _multimedia in multimedia_list:
            _multimedia.provider = provider
            db.session.add(_multimedia)
            db.session.commit()

        _submitted_count = 0
        _to_subtract = 0
        for collection_item in abcd_model.collection_items:

            _unit_id_item = collection_item.get_attribute(c.attrs[c.name_unit_id]['name'])
            _unit_id = int(_unit_id_item.values[0]) if _unit_id_item.values[0].isdigit() else None
            _collection_db = db.session.query(Collection).filter_by(
                                            unit_id_numeric=_unit_id,
                                            provider_id=provider.id).first()
            if not _collection_db:
                collection = Collection()

                collection.unit_id_numeric = _unit_id
                collection.unit_id = collection_item.get_attribute(c.attrs[c.name_unit_id]['name']).values[0]

                collection.authorship = collection_item.get_attribute(c.attrs[c.name_authorship]['name']).values[0]

                _scientific_name = collection_item.get_attribute(c.attrs[c.name_full_scientific_name_string]['name']).values[0]
                collection.full_scientific_name = " ".join([_scientific_name,
                                                            collection.authorship if collection.authorship else ''])

                collection.taxonomy = collection_item.get_attribute(c.attrs[c.name_taxonomy]['name']).values[0]
                collection.genus = self.get_from_taxonomy(collection.taxonomy, '[Genus]: ')
                collection.species = self.get_from_taxonomy(collection.taxonomy, '[Species]: ')

                _province_str = collection_item.get_attribute(c.attrs[c.name_province]['name']).values[0]
                collection.province = " ".join([part.lower().capitalize() for part in _province_str.split()]) if _province_str is not None else ''

                _district_str = collection_item.get_attribute(c.attrs[c.name_district]['name']).values[0]
                collection.district = " ".join([part.lower().capitalize() for part in _district_str.split()]) if _district_str is not None else ''

                _date_str = collection_item.get_attribute(c.attrs[c.name_last_date]['name']).values[0]

                if _date_str is not None:
                    if len(_date_str) == 4:
                        _date_str += '-01-01'
                    elif len(_date_str) == 7:
                        _date_str += '-01'

                try:
                    collection.last_date = datetime.strptime(_date_str, c.date_format) if _date_str else None
                except ValueError:
                    print('problematic data found:' + _date_str)

                collection.last_year = collection.last_year .year if collection.last_year else None

                _latitude_str = collection_item.get_attribute(c.attrs[c.name_latitude_decimal]['name']).values[0]
                collection.latitude = float(_latitude_str) if _latitude_str else None

                _longitude_str = collection_item.get_attribute(c.attrs[c.name_longitude_decimal]['name']).values[0]
                collection.longitude = float(_longitude_str) if _longitude_str else None

                collection.thumbnail_id = provider.thumbnail.multimedia_id if provider.thumbnail else None

                collection.provider = provider

                try:
                    db.session.add(collection)
                    db.session.commit()
                    _submitted_count += 1
                except Exception:
                    print('failed to submit Collection(id, unit_id) = ({}, {})'.format(collection.id, collection.unit_id))

            else:
                print('Collection(id, unit_id_numeric, provider) = ({}, {}, {}) already exists on the DB.\nUpdating it!'\
                        .format(_collection_db.id, _collection_db.unit_id_numeric, _collection_db.provider.abbreviation))
                _to_subtract += 1

            # store to the DB instead.
            # for each collection_item, check if it's on the DB: use collection_items_id
        if _to_subtract > 0:
            provider.nr_collections = provider.nr_collections - _to_subtract
            db.session.commit()

        return _submitted_count

    def get_from_taxonomy(self, taxonomy, term):
        if term not in taxonomy:
            return None

        _str_from_term = taxonomy[taxonomy.find(term) + len(term):]
        _str_term_value = _str_from_term[: _str_from_term.find(' [')]
        return _str_term_value

