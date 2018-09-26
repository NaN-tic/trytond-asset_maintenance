#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Category', 'Asset', 'Maintenance']


class Category(ModelSQL, ModelView):
    'Asset Maintenance Category'
    __name__ = 'asset.maintenance.category'
    name = fields.Char('Name', required=True)


class Asset(metaclass=PoolMeta):
    __name__ = 'asset'
    maintenances = fields.One2Many('asset.maintenance', 'asset',
        'Maintenances')


class Maintenance(ModelSQL, ModelView):
    'Asset Maintenance'
    __name__ = 'asset.maintenance'

    asset = fields.Many2One('asset', 'Asset', required=True,
        ondelete='CASCADE')
    category = fields.Many2One('asset.maintenance.category', 'Category',
        required=True)
    date_planned = fields.Date('Planned Date', states={
            'required': Eval('state') == 'planned',
            })
    date_start = fields.Date('Start Date', states={
            'required': Eval('state').in_(['in-progress', 'done']),
            })
    date_done = fields.Date('Done Date', states={
            'required': Eval('state') == 'done',
            })
    note = fields.Text('Note')
    party = fields.Many2One('party.party', 'Party')
    state = fields.Selection([
            ('planned', 'Planned'),
            ('in-progress', 'In Progress'),
            ('done', 'Done'),
            ], 'State', required=True)

    @staticmethod
    def default_state():
        return 'planned'
