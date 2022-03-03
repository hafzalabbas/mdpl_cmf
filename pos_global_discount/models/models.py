# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models



class PosConfig(models.Model):
    _inherit = 'pos.config'


    module_pos_cash_discount = fields.Boolean("Global Cash Discounts")
    iface_discount_cash = fields.Boolean(string='Order Cash Discounts',
                                         help='Allow the cashier to give cash discounts on the whole order.')
    discount_amt = fields.Float(string='Discount Amount', help='The default discount cash', default=10.0)
    cash_discount_product_id = fields.Many2one('product.product', string='Cash Discount Product',
                                          domain="[('available_in_pos', '=', True), ('sale_ok', '=', True)]",
                                          help='The product used to model the discount.')

    manual_amt_discount = fields.Boolean(string="Manual Amount Discounts", default=True)


    @api.onchange('company_id', 'module_pos_cash_discount')
    def _default_cash_discount_product_id(self):
        product = self.env.ref("point_of_sale.product_product_consumable", raise_if_not_found=False)
        self.cash_discount_product_id = product if self.module_pos_cash_discount and product and (
                    not product.company_id or product.company_id == self.company_id) else False

    @api.model
    def _default_cash_discount_value_on_module_install(self):
        configs = self.env['pos.config'].search([])
        open_configs = (
            self.env['pos.session']
                .search(['|', ('state', '!=', 'closed'), ('rescue', '=', True)])
                .mapped('config_id')
        )
        # Do not modify configs where an opened session exists.
        for conf in (configs - open_configs):
            conf._default_cash_discount_product_id()

