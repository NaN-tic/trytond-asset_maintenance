import datetime
import unittest

from proteus import Model, Wizard
from trytond.modules.company.tests.tools import create_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        today = datetime.date(2015, 1, 1)

        # Install asset_maintenance
        activate_modules('asset_maintenance')

        # Create company
        _ = create_company()

        # Create a party
        Party = Model.get('party.party')
        party = Party(name='Customer')
        party.save()
        party2 = Party(name='Customer')
        party2.save()

        # Create asset
        Asset = Model.get('asset')
        Category = Model.get('asset.maintenance.category')
        Maintenance = Model.get('asset.maintenance')
        asset = Asset()
        asset.name = 'Asset'
        asset.save()
        category = Category()
        category.name = 'Test'
        category.save()
        maintenance = Maintenance()
        maintenance.asset = asset
        maintenance.category = category
        maintenance.date_planned = today
        maintenance.party = party
        maintenance.save()

        # Try replace active party
        replace = Wizard('party.replace', models=[party])
        replace.form.source = party
        replace.form.destination = party2
        replace.execute('replace')

        # Check fields have been replaced
        maintenance.reload()
        self.assertEqual(maintenance.party, party2)
