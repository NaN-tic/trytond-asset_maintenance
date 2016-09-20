#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Category', 'Asset', 'Maintenance']
__metaclass__ = PoolMeta


class Category(ModelSQL, ModelView):
    'Asset Maintenance Category'
    __name__ = 'asset.maintenance.category'
    name = fields.Char('Name', required=True, translate=True)


class Asset:
    __name__ = 'asset'
    mantineances = fields.One2Many('asset.maintenance', 'asset',
        'Maintenances')


class Maintenance(ModelSQL, ModelView):
    'Asset Maintenance'
    __name__ = 'asset.maintenance'

    asset = fields.Many2One('asset', 'Asset', required=True,
        ondelete='CASCADE')
    category = fields.Many2One('asset.maintenance.category', 'Category',
        required=True)
    date_planned = fields.Date('Planned Date')
    date_start = fields.Date('Start Date')
    date_done = fields.Date('Done Date')
    date_next = fields.Date('Next Maintenance')
    note = fields.Text('Note')
    party = fields.Many2One('party.party', 'Party')
    reference = fields.Reference('Reference', selection='get_reference',
        select=True)
    company = fields.Function(fields.Many2One('company.company', 'Company'),
        'on_change_with_company', searcher='search_company')

    @staticmethod
    def _get_reference():
        'Return list of Model names for origin Reference'
        return []

    @classmethod
    def get_reference(cls):
        pool = Pool()
        IrModel = pool.get('ir.model')
        models = cls._get_reference()
        models = IrModel.search([
                ('model', 'in', models),
                ])
        return [(None, '')] + [(m.model, m.name) for m in models]

    @fields.depends('asset')
    def on_change_with_company(self, name=None):
        if self.asset and self.asset.company:
            return self.asset.company.id

    @classmethod
    def search_company(cls, name, clause):
        return [('asset.%s' % name,) + tuple(clause[1:])]
