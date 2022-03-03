# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    pack_type = fields.Selection(related="product_id.pack_type", )
    pack_parent_line_id = fields.Many2one(
        "stock.move.line", "Pack", help="The pack that contains this product.",
    )
    pack_depth = fields.Integer(
        "Depth", help="Depth of the product if it is part of a pack."
    )
    pack_child_line_ids = fields.One2many(
        "stock.move.line", "pack_parent_line_id", "Lines in pack"
    )
    pack_modifiable = fields.Boolean(help="The parent pack is modifiable")

    def expand_pack_line(self, write=False):
        self.ensure_one()

        if self.product_id.pack_ok and self.pack_type == "detailed":
            for subline in self.product_id.get_pack_lines():

                if write:
                    existing_subline = self.search(
                        [
                            ("product_id", "=", subline.product_id.id),
                            ("pack_parent_line_id", "=", self.id),
                        ],
                        limit=1,
                    )
                    if existing_subline:
                        vals = {
                            'qty_done': subline.quantity * self.qty_done
                        }
                        existing_subline.write(vals)
                else:
                    vals = subline.get_stock_move_line_vals(self, self.picking_id)
                    self.create(vals)

    @api.model_create_multi
    def create(self, vals):
        record = super().create(vals)
        for line in record:
            line.expand_pack_line()
        return record

    def write(self, vals):
        super().write(vals)
        if "qty_done" in vals:
            for record in self:
                record.expand_pack_line(write=True)
#
#
# class StockMove(models.Model):
#     _inherit = "stock.move"
