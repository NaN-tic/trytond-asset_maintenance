#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
import datetime
from dateutil.relativedelta import relativedelta
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['Category', 'Asset', 'Maintenance']
__metaclass__ = PoolMeta


class Category(ModelSQL, ModelView):
    'Asset Maintenance Category'
    __name__ = 'asset.maintenance.category'
    name = fields.Char('Name', required=True, translate=True)


class Asset:
    __name__ = 'asset'
    maintenance_interval = fields.Selection([
            ('none', 'Without Maintenance'),
            ('day', '01 - Day'),
            ('week', '02 - Week'),
            ('month', '03 - Month'),
            ('year', '04 - Year'),
        ], 'Maintenance Interval', required=True)
    maintenance_interval_number = fields.Integer('Maintenance Interval Count',
        states={
            'required': Eval('maintenance_interval') != 'none',
            'invisible': Eval('maintenance_interval') == 'none',
            },
        depends=['maintenance_interval'])
    mantineances = fields.One2Many('asset.maintenance', 'asset',
        'Maintenances')

    @staticmethod
    def default_maintenance_interval():
        return ''

    def compute_next_maintenance_date(self, date):
        """
        Compute new maintendance date for the asset based on date
        :param date: a date: the date of the last maintenance
        """
        date += datetime.timedelta(days=1)

        interval_number = self.maintenance_interval_number
        if self.maintenance_interval == 'day':
            interval_date = relativedelta(days=interval_number)
        elif self.maintenance_interval == 'week':
            interval_date = relativedelta(weeks=interval_number)
        elif self.maintenance_interval == 'month':
            interval_date = relativedelta(months=interval_number)
        else:  # year
            interval_date = relativedelta(years=interval_number)

        return date + interval_date - relativedelta(days=1)


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

    @fields.depends('date_planned', 'date_start', 'date_done', 'asset')
    def on_change_with_date_next(self):
        if self.asset and self.asset.maintenance_interval_number:
            date = self.date_done or self.date_start or self.date_planned
            if date:
                return self.asset.compute_next_maintenance_date(date)
