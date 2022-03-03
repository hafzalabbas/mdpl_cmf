# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def auto_pos_order_invoice(self):
        pos_orders = self.env['pos.order'].search([('state', 'in', ('paid','done')),('partner_id', '!=', False)], limit=10)
        for order in pos_orders:
            order.action_pos_order_invoice()
        return