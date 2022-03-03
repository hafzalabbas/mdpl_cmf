# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # over_credit = fields.Boolean('Allow Over Credit?')

    debt_limit = fields.Float(
        string='Max Debt', digits="Account",
        help='The partner is not allowed to have a debt more than this value')
