from odoo import models, fields


class PreviousProvider(models.Model):
    _name = 'previous.provider'
    name = fields.Char('Name')
    mobile = fields.Boolean('Mobile')
    adsl = fields.Boolean('ADSL')
    fiber = fields.Boolean('fiber')
