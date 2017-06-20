import requests
from unittest import TestCase

import xml

from bionomo_pilot.biocase.constants import Constants as c
from bionomo_pilot.biocase.abcd_parser import ABCDParser
from bionomo_pilot.biocase.models import Attribute, CollectionItem, ABCDModel, DataProvider
from bionomo_pilot.biocase.query import Query


class TestFetch(TestCase):
    def create_app(self):
        pass

    def test_fetch(self):
        headers = {
            'Content-Encoding': 'utf-8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        urls = [
            'http://localhost/biocase/pywrapper.cgi?dsa=pafa_biocase',
        ]

        data = {'query': 'as'}
        response_lists = []
        for url in urls:
            r = requests.post(url, data=data, headers=headers)
            # r.tim
            r.encoding = 'utf-8'
            text_c = r.text
            parser = ABCDParser(text_c)
            response_lists.append(parser.parse_to_ABCDModel())

        self.assertTrue(len(response_lists) > 0, '')

    def test_parse_to_ABCD(self):
        headers = {
            'Content-Encoding': 'utf-8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        urls = [
            'http://localhost/biocase/pywrapper.cgi?dsa=pafa_biocase',
        ]

        query = Query('search')
        query.add_direct_seach('as')
        data = {'query': query.to_string()}

        biocase_ns_str = 'biocase_ns'
        abcd_ns_str = 'abcd_ns'
        ns = {
            biocase_ns_str: 'http://www.biocase.org/schemas/protocol/1.3',
            abcd_ns_str: 'http://www.tdwg.org/schemas/abcd/2.06',
        }

        for url in urls:
            r = requests.post(url, data=data, headers=headers)
            # r.tim
            r.encoding = 'utf-8'
            text_c = r.text
            e = xml.etree.ElementTree.fromstring(text_c.encode('utf-8'))

            # fetch 'recordCount' and 'totalSearchHits' attribute from <biocase:content> tag
            # recordCount - is the number of items (actually loaded).
            # 'totalSearchedHits' - contains recordCount + 1 (if any, else 0)
            # so the provider has more items if (totalSearchedHits) > recordCount
            content = e.find(c.abcd_path_content.format(biocase_ns_str), ns)
            record_count = content.attrib['recordCount']
            total_searched_hits = content.attrib['totalSearchHits']

            if record_count is None:
                raise ValueError('\'recordCount\' can\'t be None.')

            if total_searched_hits is None:
                raise ValueError('\'totalSearchHits\' Count can\'t be None.')

            try:
                total_searched_hits = int(total_searched_hits)
                record_count = int(record_count)
            except ValueError:
                raise ('failed to parse attributes to int. provided: {0} {1}'.format(total_searched_hits, record_count))

            technical_contact_name = e.find(
                c.abcd_path_technical_contact_name.format(biocase_ns_str, abcd_ns_str)
                , ns)
            technical_contact_name = technical_contact_name.text if technical_contact_name is not None else None
            technical_contact_email = e.find(
                c.abcd_path_technical_contact_email.format(biocase_ns_str, abcd_ns_str), ns)
            technical_contact_email = technical_contact_email.text if technical_contact_email is not None else None
            organisation_name = e.find(
                c.abcd_path_org_representation_name.format(biocase_ns_str, abcd_ns_str), ns)
            organisation_name = organisation_name.text if organisation_name is not None else None

            organisation_abbrv = e.find(
                c.abcd_path_org_representation_abbrv.format(biocase_ns_str, abcd_ns_str), ns)
            organisation_abbrv = organisation_abbrv.text if organisation_abbrv is not None else None

            units = e.findall(c.abcd_path_unit.format(biocase_ns_str, abcd_ns_str), ns)

            data_provider = DataProvider()
            data_provider.org_name = organisation_name
            data_provider.org_abbrv = organisation_abbrv
            data_provider.contact_name = technical_contact_name
            data_provider.contact_email = technical_contact_email

            abcd_model = ABCDModel()
            abcd_model.provider = data_provider
            abcd_model.total_searched_hits = total_searched_hits
            abcd_model.record_count = record_count

            for child in units:
                unit = {}
                collection_item = CollectionItem()
                collection_item.ABCD_model = abcd_model

                for key, value in c.attrs.iteritems():
                    name = c.attrs[key]['name']
                    _relative_path = c.attrs[key]['relative_path']  # this should be iterated.
                    _full_path = c.attrs[key]['full_path']  # this should be iterated.
                    value = child.find(_relative_path.format(abcd_ns_str), ns)
                    value = value.text if value is not None else None

                    unit[name] = value

                    attribute = Attribute()
                    attribute.id = key  # this will be 'k' for key (in the dict)
                    attribute.name = name
                    attribute.relative_path = _relative_path
                    attribute.full_path = _full_path
                    attribute.values = [value]

                    collection_item.add_attribute(attribute)

                abcd_model.add_collection_item(collection_item)

        self.assertTrue(len(abcd_model.collection_items) > 0, 'collection size can\'t be zero!')
