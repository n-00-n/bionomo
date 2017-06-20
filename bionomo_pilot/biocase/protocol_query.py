# encoding: utf-8
# module biocase.query
# developer: Silvino Guambe
"""The ProtocolQuery class is the interface for interacting with
the Biocase Software (service)"""
import requests

from ..biocase.abcd_parser import ABCDParser
from ..biocase.query import Query
from ..biocase.constants import Constants as c
from models import BioCaseResult

headers = {
    'Content-Encoding': 'utf-8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml',
    'Content-Type': 'application/x-www-form-urlencoded',
}

urls = [
        # 'http://localhost/biocase/pywrapper.cgi?dsa=pafa_biocase',
        # 'http://localhost/biocase/pywrapper.cgi?dsa=pafa_clone',
        # 'http://localhost/biocase/pywrapper.cgi?dsa=plants_biocase',
        # 'http://localhost/biocase/pywrapper.cgi?dsa=aifm2006_biocase',
        'http://localhost/biocase/pywrapper.cgi?dsa=mhnm_biocase'
        ]


class ProtocolQuery(object):

    def __init__(self):
        self.query_type = 'search_direct'
        self.query = Query('search')

        self.search_text = None

    def set_query_type(self):
        pass

    def set_direct_text(self, search_text):
        self.query.add_direct_seach(search_text)
        self.search_text = search_text

    def set_attribute_dict(self, attribute_dict):
        self.query.add_single_attribute(attribute_dict)
        self.search_text = attribute_dict['value']

    def load_updates(self):
        # it assumes that the id's are generated incrementally
        # reveices a list of dict: {'data-provider-id': last_id}
        #
        # for each data-provider
        #       load from local database (fixed int)
        pass

    def load_all(self):
        # returns a list of dicts containg {'data-provider-id': list_of_collection}

        # so for each data-provider:
        #   fetch all the collection as an object
        #   create a dict with {data-provider: collection_list}
        #   appends that dict to a global list
        # returns the list
        pass

    def fetch_result(self):
        """Queries and returns a BioCaseResult object"""
        biocase_rs = BioCaseResult()
        data = {'query': self.query.to_string()}
        for url in urls:
            r = requests.post(url, data=data, headers=headers)
            r.encoding = 'utf-8'
            parser = ABCDParser(r.text)
            abcd_model = parser.parse_to_ABCDModel()

            while abcd_model.has_more_items:

                attribute_dict = {
                    'path': c.full_path_unit_id,
                    'operation': c.query_conjuction_op_greather_than_tag,
                    'value': abcd_model.flag
                }

                self.set_attribute_dict(attribute_dict)
                data = {'query': self.query.to_string()}

                r = requests.post(url, data=data, headers=headers)
                r.encoding = 'utf-8'
                parser = ABCDParser(r.text)
                _new_abcd_model = parser.parse_to_ABCDModel()
                _new_abcd_model.extend_collection_items(abcd_model.collection_items)

                abcd_model = _new_abcd_model

            biocase_rs.attach_abcd_model(abcd_model)

        return biocase_rs

    def fetch_result_as_ABCDModels(self, flag=None):
        """Queries and returns a list of ABCDModel
        Loads the initial block only."""
        data = {'query': self.query.to_string()}
        abcd_model_list = []
        for url in urls:
            r = None
            try:
                r = requests.post(url, data=data, headers=headers, timeout=15)
            except:
                pass

            if r:
                r.encoding = 'utf-8'
                parser = ABCDParser(r.text)

                abcd_model = parser.parse_to_ABCDModel()
                abcd_model.provider.url = url
                abcd_model_list.append(abcd_model)
            else:
                print 'request for [{}] failed'.format(url)

        return abcd_model_list

    def load_more_from_ABCDModel(self, abcd_model, attribute_dict):
        if abcd_model.has_more_items and abcd_model.flag:

            self.query.add_single_attribute(attribute_dict)
            data = {'query': self.query.to_string()}

            try:
                r = requests.post(abcd_model.provider.url, data=data, headers=headers, timeout=15)
            except:
                pass

            if r:
                r.encoding = 'utf-8'
                parser = ABCDParser(r.text)

                _abcd_model = parser.parse_to_ABCDModel()
                _abcd_model.provider.url = abcd_model.provider.url

                return _abcd_model

    def fetch_csv_data(self):
        list = self.fetch_result()['list']

        _output = ''
        for l in list:
            _output += l['FullScientificNameString'] + ',' + l['LatitudeDecimal'] + ',' + l['LongitudeDecimal'] + '\n'

        return _output
        # return 'teste,test2,test3\ntest4,test5,test6\n'
