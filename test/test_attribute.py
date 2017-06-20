from unittest import TestCase
from bionomo_pilot.models import Attribute


class TestAttribute(TestCase):
    def test_attribute_basic(self):
        """Basic test to set up"""
        attribute = Attribute('at-03', 'FullScientificNameString')
        self.assertEquals(attribute.code, 'at-03')
