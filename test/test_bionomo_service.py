from flask_testing import TestCase

from bionomo_pilot import *


class TestBioNoMoService(TestCase):
    def create_app(self):
        return create_app('dev')
        # return create_app('test')  # this takes too much time running. dunno why though!

    def setUp(self):
        # Components.db.create_all()
        pass

    def tearDown(self):
        # Components.db.drop_all()
        # Components.db.session.remove()
        pass

    def test_get_logo_by_name(self):
        from bionomo_pilot.service.bionomo_service import BioNoMoService
        from bionomo_pilot.models import Multimedia
        from bionomo_pilot.constants import Constants as c

        Components.db.session.add(
            Multimedia(short_name='logo_uem', full_name='uem-logo.jpg')
        )

        service = BioNoMoService()
        image = service.get_image('logo_uem', c.CODE_IMG_LOGO)

        self.assertEqual(image.name, 'logo_uem')

    def test_get_partner_stats(self):
        from bionomo_pilot.service.bionomo_service import BioNoMoService

        service = BioNoMoService()

        self.assertGreater(len(service.get_partner_stats()), 0)

    def test_get_providers_top(self):
        from bionomo_pilot.service.bionomo_service import BioNoMoService

        service = BioNoMoService()
        providers = service.get_providers()
        self.assertEqual(len(providers[0].collection_list.limit(5).all()), 5)

