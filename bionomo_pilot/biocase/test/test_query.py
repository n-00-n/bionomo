from unittest import TestCase

from ..constants import Constants
from ..models import Attribute
from ..query import Query


class TestQuery(TestCase):
    def test_direct_search_query(self):
        # Make the class is being properly initialized
        self.assertRaises(ValueError, lambda: Query('as'))

        query = Query('search')
        query.add_direct_seach('as')

        _expected_str = '''<?xml version='1.0' encoding='utf-8'?>
                            <request xmlns="http://www.biocase.org/schemas/protocol/1.3">
                              <header>
                                <type>search</type>
                              </header>
                              <search>
                                <requestFormat>http://www.tdwg.org/schemas/abcd/2.06</requestFormat>
                                <responseFormat limit="10" start="0">http://www.tdwg.org/schemas/abcd/2.06</responseFormat>
                                <count>false</count>
                                <filter>
                                  <like path="/DataSets/DataSet/Units/Unit/SpecimenUnit/NomenclaturalTypeDesignations/NomenclaturalTypeDesignation/TypifiedName/FullScientificNameString">as*</like>
                                </filter>
                              </search>
                            </request>'''.replace(' ', '').replace('\n', '')

        self.assertEqual(query.to_string().replace(' ', '').replace('\n', ''), _expected_str)

    def test_conjuction_query_with_attribute(self):
        self.assertRaises(ValueError, lambda: Query('tes'))

        query = Query('search')
        # well, basically here i'm creating attribute list to test the
        # query.add_conjuction_query.
        # should do it today... but gotta do other stuffs. :). I'm looking forward for it though!
        attributes = [
            Attribute('at_03', operation='')
        ]

        _params = {
            Constants.query_advanced_search_aquisition_date_fixed_code: ('1951-07-24', Constants.query_conjuction_op_equal_code),
            Constants.query_advanced_search_genus_code: ('Bati', Constants.query_conjuction_op_like_middle_code),
            Constants.query_advanced_search_aquisition_from_fixed_code: ('Veiga', Constants.query_conjuction_op_like_middle_code),
        }

        query.add_conjuction_query(_params)

        _expected_result = """<?xml version='1.0' encoding='utf-8'?>
                                <request xmlns="http://www.biocase.org/schemas/protocol/1.3">
                                  <header>
                                    <type>search</type>
                                  </header>
                                  <search>
                                    <requestFormat>http://www.tdwg.org/schemas/abcd/2.06</requestFormat>
                                    <responseFormat limit="10" start="0">http://www.tdwg.org/schemas/abcd/2.06</responseFormat>
                                    <count>false</count>
                                    <filter>
                                      <and>
                                        <like path="/DataSets/DataSet/Units/Unit/SpecimenUnit/NomenclaturalTypeDesignations/NomenclaturalTypeDesignation/TypifiedName/NameAtomised/Zoological/GenusOrMonomial">*Bati*</like>
                                        <equals path="/DataSets/DataSet/Units/Unit/SpecimenUnit/Acquisition/AcquisitionDate">1951-07-24</equals>
                                        <like path="/DataSets/DataSet/Units/Unit/SpecimenUnit/Acquisition/AcquiredFrom/Person/FullName">*Veiga*</like>
                                      </and>
                                    </filter>
                                  </search>
                                </request>""".replace(' ', '').replace('\n', '')

        self.assertEqual(query.to_string().replace(' ', '').replace('\n', ''), _expected_result)

    def test_combined_conjunction_query(self):
        self.assertRaises(ValueError, lambda: Query('ase'))

        query = Query('search')

        _params1 = {
            Constants.query_advanced_search_aquisition_date_fixed_code: (
            '1951-07-24', Constants.query_conjuction_op_equal_code),
            Constants.query_advanced_search_genus_code: ('Bati', Constants.query_conjuction_op_like_middle_code),
            Constants.query_advanced_search_aquisition_from_fixed_code: (
            'Veiga', Constants.query_conjuction_op_like_middle_code),
        }
        _params2 = {
            Constants.query_advanced_search_genus_code: ('Tchagra', Constants.query_conjuction_op_like_middle_code),
            Constants.query_advanced_search_aquisition_from_fixed_code: (
            'Pelao', Constants.query_conjuction_op_like_middle_code),
        }

        parameters = [_params1, _params2]
        query.add_combined_conjunction_query(parameters)

        _expected_result = """<?xml version='1.0' encoding='utf-8'?>
                                <request xmlns="http://www.biocase.org/schemas/protocol/1.3">
                                  <header>
                                    <type>search</type>
                                  </header>
                                  <search>
                                    <requestFormat>http://www.tdwg.org/schemas/abcd/2.06</requestFormat>
                                    <responseFormat limit="10" start="0">http://www.tdwg.org/schemas/abcd/2.06</responseFormat>
                                    <count>false</count>
                                    <filter>
                                      <or>
                                        <and>
                                          <like path="/DataSets/DataSet/Units/Unit/SpecimenUnit/NomenclaturalTypeDesignations/NomenclaturalTypeDesignation/TypifiedName/NameAtomised/Zoological/GenusOrMonomial">*Bati*</like>
                                          <equals path="/DataSets/DataSet/Units/Unit/SpecimenUnit/Acquisition/AcquisitionDate">1951-07-24</equals>
                                          <like path="/DataSets/DataSet/Units/Unit/SpecimenUnit/Acquisition/AcquiredFrom/Person/FullName">*Veiga*</like>
                                        </and>
                                        <and>
                                          <like path="/DataSets/DataSet/Units/Unit/SpecimenUnit/NomenclaturalTypeDesignations/NomenclaturalTypeDesignation/TypifiedName/NameAtomised/Zoological/GenusOrMonomial">*Tchagra*</like>
                                          <like path="/DataSets/DataSet/Units/Unit/SpecimenUnit/Acquisition/AcquiredFrom/Person/FullName">*Pelao*</like>
                                        </and>
                                      </or>
                                    </filter>
                                  </search>
                                </request>""".replace(' ', '').replace('\n', '')

        self.assertEqual(query.to_string().replace(' ', '').replace('\n', ''), _expected_result)
