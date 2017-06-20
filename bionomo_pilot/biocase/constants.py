# encoding: utf-8
# module: biocase.constants
# developer: Silvino Guambe Jr.


class Constants(object):
    # query options: search | scan | capabilities
    collection_item_limit = 500
    date_format = '%Y-%m-%d'
    query_search = 'search'
    query_scan = 'scan'
    query_capabilities = 'capabilities'
    query_options = [query_search, query_scan, query_capabilities]

    # ABCD concepts configuration
    # prefix 0,1: avoid crash with other configs
    # Advanced query options
    # codes for faster comparison
    # todo: obsolete this!
    query_advanced_search_province_code = 0
    query_advanced_search_genus_code = 1
    query_advanced_search_family_code = 2
    query_advanced_search_higher_taxon_code = 3
    query_advanced_search_locality_code = 4
    query_advanced_search_collector_code = 5
    query_advanced_search_collection_year_fixed_code = 6
    query_advanced_search_collection_year_range_start_code = 7
    query_advanced_search_collection_year_range_end_code = 8
    query_advanced_search_collector_number_code = 9
    query_advanced_search_field_number_code = 10
    query_advanced_search_aquisition_date_fixed_code = 11
    query_advanced_search_aquisition_from_fixed_code = 12

    # paths for the codes
    query_advanced_search_province_path = './'
    query_advanced_search_genus_path = '/DataSets/DataSet/Units/Unit/SpecimenUnit/NomenclaturalTypeDesignations/NomenclaturalTypeDesignation/TypifiedName/NameAtomised/Zoological/GenusOrMonomial'
    query_advanced_search_family_path = './'
    query_advanced_search_higher_taxon_path = './'
    query_advanced_search_locality_path = './'
    query_advanced_search_collector_path = './'
    query_advanced_search_aquisition_date_fixed_path = '/DataSets/DataSet/Units/Unit/SpecimenUnit/Acquisition/AcquisitionDate'
    query_advanced_search_aquisition_from_fixed_path = '/DataSets/DataSet/Units/Unit/SpecimenUnit/Acquisition/AcquiredFrom/Person/FullName'
    query_advanced_search_collection_year_fixed_path = './'
    query_advanced_search_collection_year_range_start_path = './'
    query_advanced_search_collection_year_range_end_path = './'
    query_advanced_search_collector_number_path = './'
    query_advanced_search_field_number_path = './'

    # dict for code => path
    query_advanced_search_dict = {
        query_advanced_search_province_code: query_advanced_search_province_path,
        query_advanced_search_genus_code: query_advanced_search_genus_path,
        query_advanced_search_family_code: query_advanced_search_family_path,
        query_advanced_search_higher_taxon_code: query_advanced_search_higher_taxon_path,
        query_advanced_search_locality_code: query_advanced_search_locality_path,
        query_advanced_search_collector_code: query_advanced_search_collector_path,
        query_advanced_search_collection_year_fixed_code: query_advanced_search_collection_year_fixed_path,
        query_advanced_search_collection_year_range_start_code: query_advanced_search_collection_year_range_start_path,
        query_advanced_search_collection_year_range_end_code: query_advanced_search_collection_year_range_end_path,
        query_advanced_search_collector_number_code: query_advanced_search_collector_number_path,
        query_advanced_search_field_number_code: query_advanced_search_field_number_path,
        query_advanced_search_aquisition_date_fixed_code: query_advanced_search_aquisition_date_fixed_path,
        query_advanced_search_aquisition_from_fixed_code: query_advanced_search_aquisition_from_fixed_path,
    }

    # operations on the query form.
    # prefix 3: to avoid crash (in case of mistyipng) with other configs
    query_conjuction_op_like_code = 20
    query_conjuction_op_like_end_code = 21
    query_conjuction_op_like_middle_code = 22
    query_conjuction_op_equal_code = 23

    # prefix 3: to avoid crash (in case of mistyipng) with other configs
    query_conjuction_op_like_tag = 'like'
    query_conjuction_op_equal_tag = 'equals'
    query_conjuction_op_greather_than_tag = 'greaterThan'
    query_conjuction_op_greather_than_or_equals_tag = 'greaterThanOrEquals'
    query_conjuction_op_less_than_tag = 'lessThan'
    query_conjuction_op_less_than_or_equals_tag = 'lessThanOrEquals'

    query_conjuction_op_tag_dict = {
        query_conjuction_op_like_code: query_conjuction_op_like_tag,
        query_conjuction_op_like_middle_code: query_conjuction_op_like_tag,
        query_conjuction_op_like_end_code: query_conjuction_op_like_tag,
        query_conjuction_op_equal_code: query_conjuction_op_equal_tag,
    }

    query_conjuction_op_content_dict = {
        query_conjuction_op_equal_code: "{}",
        query_conjuction_op_like_code: "{}*",
        query_conjuction_op_like_middle_code: "*{}*",
        query_conjuction_op_like_end_code: "*{}",
    }

    # parsing
    # id name path value
    # the names
    abcd_path_technical_contact_email = './{0}:content/{1}:DataSets/{1}:DataSet' \
                                        '/{1}:TechnicalContacts/{1}:TechnicalContact/{1}:Email'

    abcd_path_org_representation_name = './{0}:content/{1}:DataSets/{1}:DataSet' \
                                        '/{1}:Metadata/{1}:Owners/{1}:Owner' \
                                        '/{1}:Organisation/{1}:Name/{1}:Representation/{1}:Text'

    abcd_path_org_representation_abbrv = './{0}:content/{1}:DataSets/{1}:DataSet' \
                                         '/{1}:Metadata/{1}:Owners/{1}:Owner' \
                                         '/{1}:Organisation/{1}:Name/{1}:Representation/{1}:Abbreviation'

    abcd_path_org_address = './{0}:content/{1}:DataSets/{1}:DataSet' \
                                         '/{1}:Metadata/{1}:Owners/{1}:Owner' \
                                         '/{1}:Addresses/{1}:Address'

    abcd_path_unit = './{0}:content/{1}:DataSets/{1}:DataSet' \
                     '/{1}:Units/{1}:Unit'
    # path after the /Unit
    abcd_path_unit_institution_source_id = '{0}:SourceInstitutionID'
    abcd_path_unit_source_id = '{0}:SourceID'

    abcd_path_content = './{0}:content'
    abcd_path_technical_contact_name = './{0}:content/{1}:DataSets/{1}:DataSet' \
                                       '/{1}:TechnicalContacts/{1}:TechnicalContact/{1}:Name'

    _name_prefix = 'at'

    _count = 1
    name_content = '_'.join([_name_prefix, '%02d' % _count])


    _count += 1
    name_unit_id_numeric = '_'.join([_name_prefix, '%02d' % _count])
    full_path_unit_id_numeric = '/DataSets/DataSet/Units/Unit' \
                                 '/UnitIDNumeric'
    abcd_path_unit_id_numeric = '{}:UnitIDNumeric'

    _count += 1
    name_unit_id = '_'.join([_name_prefix, '%02d' % _count])
    full_path_unit_id = '/DataSets/DataSet/Units/Unit' \
                                 '/UnitID'
    abcd_path_unit_id = '{}:UnitID'

    _count += 1
    name_acquisition_date = '_'.join([_name_prefix, '%02d' % _count])
    full_path_acquisition_date = '/DataSets/DataSet/Units/Unit' \
                                 '/SpecimenUnit/Acquisition/' \
                                 'AcquisitionDate'
    abcd_path_unit_acquisition_date = '{0}:SpecimenUnit/{0}:Acquisition' \
                                      '/{0}:AcquisitionDate'

    _count += 1
    name_acquisition_person = '_'.join([_name_prefix, '%02d' % _count])
    full_path_acquisition_person = '/DataSets/DataSet/Units/Unit' \
                                   '/SpecimenUnit/Acquisition/' \
                                   'AcquiredFrom/Person/FullName'
    abcd_path_unit_acquisition_person = '{0}:SpecimenUnit/{0}:Acquisition' \
                                        '/{0}:AcquiredFrom/{0}:Person/{0}:FullName'

    _count += 1
    name_acquisition_address = '_'.join([_name_prefix, '%02d' % _count])
    full_path_acquisition_address = '/DataSets/DataSet/Units/Unit' \
                                    '/SpecimenUnit/Acquisition/' \
                                    'AcquiredFrom/Addresses/Address'
    abcd_path_unit_acquisition_address = '{0}:SpecimenUnit/{0}:Acquisition' \
                                         '/{0}:AcquiredFrom/{0}:Addresses/{0}:Address'

    _count += 1
    name_preparation_process = '_'.join([_name_prefix, '%02d' % _count])
    full_path_preparation_process = '/DataSets/DataSet/Units/Unit' \
                                    '/SpecimenUnit/Preparations/' \
                                    'Preparation/PreparationProcess'
    abcd_path_unit_preparation_process = '{0}:SpecimenUnit/{0}:Preparations' \
                                         '/{0}:Preparation/{0}:PreparationProcess'

    _count += 1
    name_contacts_org_name = '_'.join([_name_prefix, '%02d' % _count])
    full_path_contacts_org_name = '/DataSets/DataSet/Units/Unit' \
                                  '/UnitContentContacts/UnitContentContact/' \
                                  'Organisation/Name/Representation/Text'
    abcd_path_unit_contacts_org_name = '{0}:UnitContentContacts/{0}:UnitContentContact' \
                                       '/{0}:Organisation/{0}:Name/{0}:Representation/{0}:Text'

    _count += 1
    name_contacts_org_abbrv = '_'.join([_name_prefix, '%02d' % _count])
    full_path_contacts_org_abbrv = '/DataSets/DataSet/Units/Unit' \
                                   '/UnitContentContacts/UnitContentContact/' \
                                   'Organisation/Name/Representation/Abbreviation'
    abcd_path_unit_contacts_org_abbrv = '{0}:UnitContentContacts/{0}:UnitContentContact' \
                                        '/{0}:Organisation/{0}:Name/{0}:Representation/{0}:Abbreviation'

    _count += 1
    name_full_scientific_name_string = '_'.join([_name_prefix, '%02d' % _count])
    query_direct_search_path = '/DataSets/DataSet/Units/Unit/Identifications/' \
                               'Identification/Result/TaxonIdentified/ScientificName' \
                               '/FullScientificNameString'
    full_path_full_scientific_name = query_direct_search_path
    abcd_path_unit_full_scientific_name_string = '{0}:Identifications/{0}:Identification' \
                                                 '/{0}:Result/{0}:TaxonIdentified/{0}:ScientificName' \
                                                 '/{0}:FullScientificNameString'

    _count += 1
    name_genus_or_monomial = '_'.join([_name_prefix, '%02d' % _count])
    full_path_genus_or_monomial = '/DataSets/DataSet/Units/Unit' \
                                  '/SpecimenUnit/NomenclaturalTypeDesignations/' \
                                  'NomenclaturalTypeDesignation/TypifiedName' \
                                  '/NameAtomised/Zoological/GenusOrMonomial'
    abcd_path_unit_genus_or_monomial = '{0}:SpecimenUnit/{0}:NomenclaturalTypeDesignations' \
                                       '/{0}:NomenclaturalTypeDesignation/{0}:TypifiedName' \
                                       '/{0}:NameAtomised/{0}:Zoological/{0}:GenusOrMonomial'

    _count += 1
    name_species_epithet = '_'.join([_name_prefix, '%02d' % _count])
    full_path_species_epithet = '/DataSets/DataSet/Units/Unit' \
                                  '/SpecimenUnit/NomenclaturalTypeDesignations/' \
                                  'NomenclaturalTypeDesignation/TypifiedName' \
                                  '/NameAtomised/Zoological/SpeciesEpithet'
    abcd_path_unit_species_epithet = '{0}:SpecimenUnit/{0}:NomenclaturalTypeDesignations' \
                                     '/{0}:NomenclaturalTypeDesignation/{0}:TypifiedName' \
                                     '/{0}:NameAtomised/{0}:Zoological/{0}:SpeciesEpithet'

    _count += 1
    name_province = '_'.join([_name_prefix, '%02d' % _count])
    full_path_province = '/DataSets/DataSet/Units/Unit/Gathering/NamedAreas/NamedArea/AreaName'
    abcd_path_province = '{0}:Gathering/{0}:NamedAreas/{0}:NamedArea/{0}:AreaName'

    _count += 1
    name_district = '_'.join([_name_prefix, '%02d' % _count])
    full_path_district = '/DataSets/DataSet/Units/Unit/Gathering/NearNamedPlaces/NamedPlaceRelation/NearNamedPlace'
    abcd_path_district = '{0}:Gathering/{0}:NearNamedPlaces/{0}:NamedPlaceRelation/{0}:NearNamedPlace'

    _count += 1
    name_latitude_decimal = '_'.join([_name_prefix, '%02d' % _count])
    name_latitude_decimal_start = name_latitude_decimal + '_01'
    name_latitude_decimal_end = name_latitude_decimal + '_02'
    full_path_latitude_decimal = '/DataSets/DataSet/Units/Unit' \
                                 '/Gathering/SiteCoordinateSets/SiteCoordinates' \
                                 'CoordinatesLatLong/LatitudeDecimal'
    abcd_path_unit_latitude_decimal = '{0}:Gathering/{0}:SiteCoordinateSets' \
                                      '/{0}:SiteCoordinates/{0}:CoordinatesLatLong' \
                                      '/{0}:LatitudeDecimal'

    _count += 1
    name_longitude_decimal = '_'.join([_name_prefix, '%02d' % _count])
    name_longitude_decimal_start = name_longitude_decimal + '01'
    name_longitude_decimal_end = name_longitude_decimal + '02'
    full_path_longitude_decimal = '/DataSets/DataSet/Units/Unit' \
                                  '/Gathering/SiteCoordinateSets/SiteCoordinates' \
                                  'CoordinatesLatLong/LongitudeDecimal'
    abcd_path_unit_longitude_decimal = '{0}:Gathering/{0}:SiteCoordinateSets' \
                                       '/{0}:SiteCoordinates/{0}:CoordinatesLatLong' \
                                       '/{0}:LongitudeDecimal'

    _count += 1
    name_first_date = '_'.join([_name_prefix, '%02d' % _count])
    name_first_date_start = name_first_date + '_01'
    name_first_date_end = name_first_date + '_02'
    full_path_first_date = '/DataSets/DataSet/Units/Unit/Gathering/DateTime/ISODateTimeBegin'
    abcd_path_first_date = '{0}:Gathering/{0}:DateTime' \
                           '/{0}:ISODateTimeBegin'

    _count += 1
    name_last_date = '_'.join([_name_prefix, '%02d' % _count])
    name_last_date_start = name_last_date + '_01'
    name_last_date_end = name_last_date + '_02'
    full_path_last_date = '/DataSets/DataSet/Units/Unit/Gathering/DateTime/ISODateTimeBegin'
    abcd_path_last_date = '{0}:Gathering/{0}:DateTime' \
                          '/{0}:ISODateTimeEnd'

    _count += 1
    name_first_year = '_'.join([_name_prefix, '%02d' % _count])
    full_path_first_year = ''
    abcd_path_first_year = ''

    _count += 1
    name_last_year = '_'.join([_name_prefix, '%02d' % _count])
    full_path_last_year = ''
    abcd_path_last_year = ''

    _count += 1
    name_authorship = '_'.join([_name_prefix, '%02d' % _count])
    full_path_authorship = '/DataSets/DataSet/Units/Unit/Identifications' \
                           '/Identification/Result/TaxonIdentified/ScientificName' \
                           '/NameAtomised/Botanical/AuthorTeam'
    abcd_path_authorship = '{0}:Identifications/{0}:Identification' \
                           '/{0}:Result/{0}:TaxonIdentified/{0}:ScientificName' \
                           '/{0}:NameAtomised/{0}:Botanical/{0}:AuthorTeam'

    _count += 1
    name_taxonomy = '_'.join([_name_prefix, '%02d' % _count])
    full_path_taxonomy = '/DataSets/DataSet/Units' \
                         '/Unit/Identifications/Identification' \
                         '/Result/TaxonIdentified/ScientificName/NameAddendum'
    abcd_path_taxonomy = '{0}:Identifications/{0}:Identification' \
                           '/{0}:Result/{0}:TaxonIdentified/{0}:ScientificName' \
                           '/{0}:NameAddendum'

    _count += 1
    name_identification_person = '_'.join([_name_prefix, '%02d' % _count])
    full_path_identification_person = '/DataSets/DataSet/Units/Unit/' \
                                      'Identifications/Identification/' \
                                      'Identifiers/Identifier/PersonName/FullName'
    abcd_path_identification_person = '{0}:Identifications/{0}:Identification' \
                                      '/{0}:Identifiers/{0}:Identifier' \
                                      '/{0}:PersonName/{0}:FullName'

    _count += 1
    name_provider = '_'.join([_name_prefix, '%02d' % _count])

    attrs = {
        name_unit_id_numeric: {
            'full_path': full_path_unit_id_numeric,
            'relative_path': abcd_path_unit_id_numeric,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'UnitIDNumeric'
        },
        name_unit_id: {
            'full_path': full_path_unit_id,
            'relative_path': abcd_path_unit_id,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'UnitID'
        },
        name_acquisition_date: {
            'full_path': full_path_acquisition_date,
            'relative_path': abcd_path_unit_acquisition_date,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'AcquisitionDate'
        },
        name_acquisition_person: {
            'full_path': full_path_acquisition_person,
            'relative_path': abcd_path_unit_acquisition_person,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'AcquisitionPerson'
        },
        name_acquisition_address: {
            'full_path': full_path_acquisition_address,
            'relative_path': abcd_path_unit_acquisition_address,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'AcquisitionAddress'
        },
        name_preparation_process: {
            'full_path': full_path_preparation_process,
            'relative_path': abcd_path_unit_preparation_process,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'PreparationProcess'
        },
        name_contacts_org_name: {
            'full_path': full_path_contacts_org_name,
            'relative_path': abcd_path_unit_contacts_org_name,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'UnitContentContacts_Organisation_Name'
        },
        name_contacts_org_abbrv: {
            'full_path': full_path_contacts_org_abbrv,
            'relative_path': abcd_path_unit_contacts_org_abbrv,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'UnitContentContacts_Organisation_Abbrv'
        },
        name_full_scientific_name_string: {
            'full_path': full_path_full_scientific_name,
            'relative_path': abcd_path_unit_full_scientific_name_string,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'FullScientificNameString'
        },
        name_genus_or_monomial: {
            'full_path': full_path_genus_or_monomial,
            'relative_path': abcd_path_unit_genus_or_monomial,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'GenusOrMonomial'
        },
        name_species_epithet: {
            'full_path': full_path_species_epithet,
            'relative_path': abcd_path_unit_species_epithet,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'SpeciesEpithet'
        },
        name_latitude_decimal: {
            'full_path': full_path_latitude_decimal,
            'relative_path': abcd_path_unit_latitude_decimal,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'LatitudeDecimal'
        },
        name_longitude_decimal: {
            'full_path': full_path_longitude_decimal,
            'relative_path': abcd_path_unit_longitude_decimal,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'LongitudeDecimal'
        },
        name_province: {
            'full_path': full_path_province,
            'relative_path': abcd_path_province,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'Province'
        },
        name_district: {
            'full_path': full_path_district,
            'relative_path': abcd_path_district,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'District'
        },
        name_first_date: {
            'full_path': full_path_first_date,
            'relative_path': abcd_path_first_date,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'FirstDate'
        },
        name_last_date: {
            'full_path': full_path_last_date,
            'relative_path': abcd_path_last_date,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'LastDate'
        },
        name_authorship: {
            'full_path': full_path_authorship,
            'relative_path': abcd_path_authorship,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'Authorship'
        },
        name_taxonomy: {
            'full_path': full_path_taxonomy,
            'relative_path': abcd_path_taxonomy,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'Taxonomy'
        },
        name_identification_person: {
            'full_path': full_path_identification_person,
            'relative_path': abcd_path_identification_person,
            'value': None,  # this should be a tuple or list, containing one or more values
            'default_operation': None,   # todo: deprecate this. No longer needed since the filter is done on DB level.
            'name': 'IdentificationPerson'
        },
    }

    request_headers = {
        'Content-Encoding': 'utf-8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data_provider_urls = [
            'http://localhost/biocase/pywrapper.cgi?dsa=pafa_biocase',
            'http://localhost/biocase/pywrapper.cgi?dsa=pafa_clone',
            'http://localhost/biocase/pywrapper.cgi?dsa=plants_biocase',
        ]
