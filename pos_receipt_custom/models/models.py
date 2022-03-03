# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    box_product = fields.Boolean(default=False, string='Is a Box?', help='Is a Box?')


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def get_onhand_box_details(self, client, current_order_box):
        if not client.get('id'):
            return False
        onhand_details = []
        box_product = {}
        pos_order_line = self.env['pos.order.line'].search([("order_id.partner_id", "=", client['id']), ("product_id.box_product", "=", True)])
        for line in pos_order_line:
            if line.product_id.id not in box_product:
                box_product[line.product_id.id] = line.qty
            else:
                box_product[line.product_id.id] += line.qty
        stock_move_line = self.env['stock.move'].search([("picking_id.partner_id", "=", client['id']),('state','=','done'),("product_id.box_product", "=", True)])
        for lines in stock_move_line:
            if lines.sale_line_id:
                if (lines.to_refund == False or not lines.to_refund) and not lines.origin_returned_move_id:
                    if lines.product_id.id not in box_product:
                        box_product[lines.product_id.id] = lines.product_uom_qty
                    else:
                        box_product[lines.product_id.id] += lines.product_uom_qty

        # if current_order_box:
        #     for box in current_order_box:
        #         if int(box) in box_product:
        #             box_product[int(box)] += current_order_box[box]
        #         else:
        #             box_product[int(box)] = current_order_box[box]
        if current_order_box:
            for box in current_order_box:
                if int(box) not in box_product:
                    box_product[int(box)] = 0
        current_bill = 0
        for box_id in box_product:
            onhand_details.append(
                {
                    'product_id': box_id,
                    'name': self.env['product.product'].browse(box_id).name,
                    'qty': box_product[box_id],
                    'current_bill': current_bill,
                    'total': current_bill+box_product[box_id],
                }
            )
        if current_order_box:
            for details in onhand_details:
                for box in current_order_box:
                    if int(box) == details['product_id']:
                        details['current_bill'] += current_order_box[box]
                        details['total'] += current_order_box[box]

        return onhand_details
