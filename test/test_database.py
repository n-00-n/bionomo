from unittest import TestCase
from bionomo_pilot.models import create_all


class DatabaseTest(TestCase):

    def create_database_structure(self):
        create_all()
