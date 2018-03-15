# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AssetMaintenanceTestCase(ModuleTestCase):
    'Test Asset Maintenance module'
    module = 'asset_maintenance'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AssetMaintenanceTestCase))
    return suite
