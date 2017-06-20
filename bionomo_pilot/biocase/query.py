# encoding: utf-8
# module biocase.query
# developer: Silvino Guambe Jr.
"""Class responsible for generating query parameter"""
# imports
from lxml import etree as et

from .constants import Constants


class Query(object):
    """
    Implementation of some features of the BioCase query capabilities.
    For simplicity all <filter> sub-elements are one of the following:
        -=[ like | equals | and | or ]=-
    """

    def __init__(self, request_type):
        """takes the 'request_type' and builds a query for request based on that.
        Can be 'search', 'scan', or 'capabilities'.
        Refer to the documentation on the BioCase website"""
        self.request_type = request_type
        if not self.validate_request_type():
            raise ValueError('Invalid request Type. Valid are: search | scan | capabilities. '
                             '\nRefer to the BioCase documentation for more information.')

        self.root = et.Element("request", xmlns='http://www.biocase.org/schemas/protocol/1.3')
        header_el = et.SubElement(self.root, 'header')
        et.SubElement(header_el, 'type').text = request_type
        self.core_el = et.SubElement(self.root, request_type)

        self.compose_core_element()

        et.SubElement(self.core_el, 'count').text = 'false'

    def compose_core_element(self):
        if self.request_type == Constants.query_search:
            self.construct_build_seach()
        elif self.request_type == Constants.query_scan:
            self.construct_build_scan()
        elif self.request_type == Constants.query_capabilities:
            self.construct_build_capabilities()

    def construct_build_seach(self):
        """Creates the 'search' tag. For querying for units.
        Please refer to the BioCase documentation for more information."""
        et.SubElement(self.core_el, 'requestFormat').text = 'http://www.tdwg.org/schemas/abcd/2.06'
        et.SubElement(self.core_el, 'responseFormat', start='0',
                      limit=str(Constants.collection_item_limit)).text = 'http://www.tdwg.org/schemas/abcd/2.06'

    def add_direct_seach(self, search_text):
        """Sets a <like>* on the filter. Work as the main filter"""
        _path = Constants.query_direct_search_path
        if self.core_el is not None:
            filter_el = et.SubElement(self.core_el, 'filter')
            et.SubElement(filter_el, Constants.query_conjuction_op_like_tag, path=_path).text = search_text + '*'
        else:
            raise SyntaxError('Initialize the object properly.')

    def add_single_attribute(self, attribute_dict):
        if self.core_el is not None:
            #first remove all the '<filter>' occurences:
            for _filter_el in self.core_el.findall('filter'):
                self.core_el.remove(_filter_el)

            #now add add a new filter_el
            filter_el = et.SubElement(self.core_el, 'filter')
            _value = str(attribute_dict['value']) + ('*' if attribute_dict['operation'] == Constants.query_conjuction_op_like_tag
                                                     else '')

            et.SubElement(filter_el, attribute_dict['operation'], path=attribute_dict['path']).text = _value
        else:
            raise SyntaxError('Initialize the object properly.')

    def add_conjuction_query(self, params_dict, parent_el=None):
        """Sets a <and> element, with <like>* sub-elements
        :param params_dict
            - dictionary: containing the {_int_code_: (_str_content_, _op_)}.
             _int_code_ = is the code for the field.
             _str_content_ = is the text to be searched
             _op_ = is the operation: 'like' or 'equals'
            ex: {Constants.query_advanced_search_province_code, ('Maputo', Constants.query_conjuction_op_like_code)}
        :param parent_el (optional)
            - optionally indicate a parent Element for the conjuction
            ex: practically to be used with <or>
        :return None
        """
        if self.core_el is not None:
            _core_el = self.core_el if parent_el is None else parent_el

            # check whether or not it should add the 'filter' tag
            if parent_el is None:
                filter_el = et.SubElement(_core_el, 'filter')
                and_el = et.SubElement(filter_el, 'and')
            else:
                and_el = et.SubElement(_core_el, 'and')

            for key, value in params_dict.iteritems():
                query_field_code = key
                query_field_content = value[0]
                query_field_op = value[1]

                _tag = Constants.query_conjuction_op_tag_dict[query_field_op]
                _path = Constants.query_advanced_search_dict[query_field_code]

                query_field_content = Constants.query_conjuction_op_content_dict[query_field_op].format(
                    query_field_content)

                et.SubElement(and_el, _tag, path=_path).text = query_field_content

    def add_conjuction_query_with_attributes(self, attribute_list, parent_el=None):
        """Sets a <and> element, with <like>* sub-elements
        :param attribute_list: list of Attribute
            - attribute: containing the {_int_code_: (_str_content_, _op_)}.
                 .code = is the code for the field. ex: 'at_03'
                 .operation = is the operation: 'like', 'equals' or 'between'
                 .values = a list/tuple of values for the operation to be applied
                ex: Attribute(code='at_03',
                              operation=constants.attrs['at_03']['default_operation'],
                              values=['macro']
                              )
        :param parent_el (optional)
            - optionally indicate a parent Element for the conjuction
            ex: practically to be used with <or>
        :return None
        """
        if self.core_el is not None:
            _core_el = self.core_el if parent_el is None else parent_el

            # check whether or not it should add the 'filter' tag
            if parent_el is None:
                filter_el = et.SubElement(_core_el, 'filter')
                and_el = et.SubElement(filter_el, 'and')
            else:
                and_el = et.SubElement(_core_el, 'and')

            for attribute in attribute_list:
                # query_field_code = attribute.path
                # query_field_content = value[0]
                # query_field_op = value[1]  # this should be replaced by attribute.operation

                # the operation should be the same as with the previous one.
                # the attribute.operation holds the operation_code
                _tag = Constants.query_conjuction_op_tag_dict[
                    attribute.operation]  # this should contain the operation content ''
                # _tag = Constants.query_conjuction_op_tag_dict[query_field_op]
                _path = attribute.path

                # check if there's only one value.
                if len(attribute.values) == 1:
                    query_field_content = Constants.query_conjuction_op_content_dict[attribute.operation].format(
                        attribute.values[0])
                else:
                    # todo: implement this. when there are more values on attributes. ex: x1 < latitude < x2, or localidade in ['Maputo', 'Gaza']
                    # this is going to be fun!
                    query_field_content = ''

                et.SubElement(and_el, _tag, path=_path).text = query_field_content

    def add_combined_conjunction_query(self, params_list):
        """
        Sets a <and> element, with <and> sub-elements
        :param params_list:
            - list of dictionary with the following structure (same used in the add_conjuction_query() method)
                - dictionary: containing the {_int_code_: (_str_content_, _op_)}.
                 _int_code_ = is the code for the field.
                 _str_content_ = is the text to be searched
                 _op_ = is the operation: 'like' or 'equals'
                ex: {Constants.query_advanced_search_province_code, ('Maputo', Constants.query_conjuction_op_like_code)}
        :return None
        """
        if not params_list:
            raise ValueError('No valid parameter provided: Please provide a list of dictionaries!')

        if self.core_el is not None:
            filter_el = et.SubElement(self.core_el, 'filter')
            or_el = et.SubElement(filter_el, 'or')
            for param in params_list:
                self.add_conjuction_query(param, or_el)

    def to_string(self):
        return et.tostring(self.root, xml_declaration=True, encoding='utf-8', pretty_print=True)

    def construct_build_scan(self, core_el):
        """Not implemented yet."""
        pass

    def construct_build_capabilities(self):
        """Not implemented yet."""
        pass

    def validate_request_type(self):
        return self.request_type in Constants.query_options
