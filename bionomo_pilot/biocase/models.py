class BioCaseResult(object):
    """Represents the Results for all queried data providers"""
    def __init__(self):
        self.nr_records = None
        self.abdc_models = []
        self.collection_items = []

    def attach_abcd_model(self, abcd_model):
        self.abdc_models.append(abcd_model)
        self.collection_items.extend(abcd_model.collection_items)


class ABCDModel:
    """Represents a model for a single data provider.
    Keeps record of the count for each data provider"""
    def __init__(self):
        self.provider = None   # provider: (org_name, org_abbrv, technical_contact_email, technical_contact_email)
        self.total_searched_hits = None
        self.record_count = None
        self.record_dropped = None
        self.collection_items = []
        self.flag = None

    @property
    def has_more_items(self):
        if self.record_count is None or self.total_searched_hits is None:
            raise RuntimeError('No recordCount, recordDropped or totalSeachedHits available to make proper comparison.')
        return self.total_searched_hits > (self.record_count + self.record_dropped)  # record_dropped usually is a negative number

    def add_collection_item(self, item):
        self.collection_items.append(item)

    def extend_collection_items(self, items_list):
        self.collection_items.extend(items_list)


class DataProvider:
    """Data provider's information"""
    def __init__(self, org_name=None, org_abbrv=None, org_address=None, contact_name=None, contact_email=None):
        self.org_name = org_name
        self.org_abbrv = org_abbrv
        self.address = org_address
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.url = None


class CollectionItem:
    """Representing each collection item. ex: specimen, etc."""
    # todo: list all the common attributes
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.ABCD_model = None  # the refering ABCD model
        self.type = None  # the type of the item. Specimen, etc
        self.attributes = {}  # the list of attributes specific to the Item: this should be a fixed list for each item's type

    def add_attribute_from_dict(self, attribute_dict):
        attribute = Attribute()
        attribute.id = attribute_dict['id']
        attribute.name = attribute_dict['name']
        attribute.relative_path = attribute_dict['relative_path']
        attribute.full_path = attribute_dict['full_path']
        attribute.value = attribute_dict['value']

        self.attributes[attribute.name] = attribute

    def add_attribute(self, attribute):
        self.attributes[attribute.name] = attribute

    def get_attribute(self, name):
        return self.attributes.get(name, None)


class Attribute:
    def __init__(self, code=None, operation=None, name=None, relative_path=None, full_path=None, values=[]):
        self.code = code    # code of the id. ex: 'at_03'
        # todo: remember this: the attribute.operation holds the operation_code
        self.operation = operation    # Operation to be applied when querying the Data Provider, 'eq', 'gt', 'lt'.
        self.name = name    # the attribute's name, ex: FullScientificName. todo: deprecate this later
        self.relative_path = relative_path    # the corresponding ABCD Xpath. the Full Path
        self.full_path = full_path    # the corresponding ABCD Xpath. the Full Path
        self.values = values    # the value on the xml or form. this should a tuple or a list of values.

    def to_render_dict(self):
        return self.name, self.values


# todo: create a model with specific attributes based on the CollectionItem obj.
# this will allow data providers to display specific information if available.
