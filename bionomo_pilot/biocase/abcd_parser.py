# encoding: utf-8
# module biocase.query
# developer: Silvino Guambe Jr.
"""Parser class responsible for parsing ABCD document to objects and dictionaries"""
import xml.etree.ElementTree
from constants import Constants as c
from models import ABCDModel, CollectionItem, Attribute, DataProvider

"""
This module is responsible for parsing the ABCDDocument to object models.

returns: ABCDModel
"""


class ABCDParser(object):
    """Document parser.
    TODO: improve performance by perhaps merging the parse_to_ABCD() with parse_to_dict()"""

    def __init__(self, xml_text):
        self.xml_str = xml_text
        self.biocase_ns_str = 'biocase_ns'
        self.abcd_ns_str = 'abcd_ns'
        self.ns = {
            self.biocase_ns_str: 'http://www.biocase.org/schemas/protocol/1.3',
            self.abcd_ns_str: 'http://www.tdwg.org/schemas/abcd/2.06',
        }

    def parse_to_ABCDModel(self):
        """Very raw implementation of the parser"""

        if self.xml_str is None:
            raise TypeError('Expected \'str\' type \'None\' provided!')

        e = xml.etree.ElementTree.fromstring(self.xml_str.encode('utf-8'))

        content = e.find(c.abcd_path_content.format(self.biocase_ns_str), self.ns)
        record_count = content.attrib['recordCount']
        record_dropped = content.attrib['recordDropped']
        total_searched_hits = content.attrib['totalSearchHits']

        if record_count is None:
            raise ValueError('\'recordCount\' can\'t be None.')

        if record_dropped is None:
            raise ValueError('\'recordDropped\' can\'t be None.')

        if total_searched_hits is None:
            raise ValueError('\'totalSearchHits\' Count can\'t be None.')

        try:
            record_count = int(record_count)
            record_dropped = int(record_dropped)
            total_searched_hits = int(total_searched_hits)
        except ValueError:
            raise ('failed to parse attributes to int. provided: '
                   '{recordCount: {0}, recordDropped: {1}, totalSearchHits: {2}}'
                   .format(record_count, record_dropped, total_searched_hits))

        technical_contact_name = e.find(c.abcd_path_technical_contact_name.format(self.biocase_ns_str, self.abcd_ns_str)
                                        , self.ns)
        technical_contact_name = technical_contact_name.text if technical_contact_name is not None else None
        technical_contact_email = e.find(
            c.abcd_path_technical_contact_email.format(self.biocase_ns_str, self.abcd_ns_str), self.ns)
        technical_contact_email = technical_contact_email.text if technical_contact_email is not None else None
        organisation_name = e.find(c.abcd_path_org_representation_name.format(self.biocase_ns_str, self.abcd_ns_str),
                                   self.ns)
        organisation_name = organisation_name.text if organisation_name is not None else None

        organisation_abbrv = e.find(c.abcd_path_org_representation_abbrv.format(self.biocase_ns_str, self.abcd_ns_str),
                                    self.ns)
        organisation_abbrv = organisation_abbrv.text if organisation_abbrv is not None else None

        organisation_address = e.find(c.abcd_path_org_address.format(self.biocase_ns_str, self.abcd_ns_str), self.ns)
        organisation_address = organisation_address.text if organisation_address is not None else None

        units = e.findall(c.abcd_path_unit.format(self.biocase_ns_str, self.abcd_ns_str), self.ns)

        if organisation_name is None:
            return None

        data_provider = DataProvider()
        data_provider.org_name = organisation_name
        data_provider.org_abbrv = organisation_abbrv
        data_provider.address = organisation_address
        data_provider.contact_name = technical_contact_name
        data_provider.contact_email = technical_contact_email

        abcd_model = ABCDModel()
        abcd_model.provider = data_provider
        abcd_model.record_count = record_count
        abcd_model.record_dropped = record_dropped
        abcd_model.total_searched_hits = total_searched_hits

        for child in units:
            unit = {}
            collection_item = CollectionItem()
            collection_item.ABCD_model = abcd_model

            for key, value in c.attrs.iteritems():
                name = c.attrs[key]['name']
                _relative_path = c.attrs[key]['relative_path']  # this should be iterated.
                _full_path = c.attrs[key]['full_path']  # this should be iterated.
                value = child.find(_relative_path.format(self.abcd_ns_str), self.ns)
                value = value.text if value is not None else None

                unit[name] = value

                attribute = Attribute()
                attribute.id = key  # this will be 'k' for key (in the dict)
                attribute.name = name
                attribute.relative_path = _relative_path
                attribute.full_path = _full_path
                attribute.values = [value]

                collection_item.add_attribute(attribute)

                if name == 'SourceInstitutionID' and data_provider.org_abbrv is None:
                    data_provider.org_abbrv = value

            abcd_model.add_collection_item(collection_item)

            abcd_model.flag = max([int(collection_item.get_attribute(c.attrs[c.name_unit_id]['name']).values[0])
                                   for collection_item in abcd_model.collection_items])

        return abcd_model
