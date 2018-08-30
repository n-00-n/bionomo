from flask_testing import TestCase
from bionomo_pilot import *


class TestDatabaseService(TestCase):

    def create_app(self):
        return create_app('dev')

    def test_create_database_structure(self):
        from bionomo_pilot.models import create_all

        create_all()