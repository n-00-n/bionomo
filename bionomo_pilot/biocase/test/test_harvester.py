from flask_testing import TestCase
# from unittest import TestCase
from bionomo_pilot import *
from bionomo_pilot.harvester.harvester import Harvester


class TestHarvester(TestCase):
    def create_app(self):
        return create_app('dev')

    def test_load_top_10(self):
        harvester = Harvester()
        self.assertGreater(len(harvester.load_top_10()), 0, 'Top 10 has to have data.')

    def test_load_and_parse(self):
        harvester = Harvester()
        self.assertGreater(len(harvester.load_and_parse()), 0, '\'harvester.load_and_parse()\' has to have data.')

    def test_load_parse_and_submit(self):
        harvester = Harvester()
        self.assertTrue(harvester.load_parse_and_submit(), '\'harvester.load_parse_and_submit()\' has to be true!.')

    def test_harvest(self):
        harvester = Harvester()
        self.assertGreater(harvester.harvest(), 0, 'harvester.harvest() must return the number of collected items. This can\'t be zero!')
