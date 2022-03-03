# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosPackOrderLine(models.Model):
    _name = "pos.pack.order.line"
    _rec_name = "product_id"

    product_id = fields.Many2one('product.product', string='Product')
    price_unit = fields.Float(string='Unit Price')
    qty = fields.Float(string='Quantity')
    discount = fields.Float(string='Discount')
    wk_order_id = fields.Many2one('pos.order', string='Order Ref', ondelete='cascade')


class PosOrder(models.Model):
    _inherit = 'pos.order'

    wk_product_pack_lines = fields.One2many('pos.pack.order.line', 'wk_order_id', string='Order Lines')

