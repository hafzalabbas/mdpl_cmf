
from odoo import fields, models


class ProductPack(models.Model):
    _inherit = "product.pack.line"

    def get_stock_move_line_vals(self, line, picking_id):
        self.ensure_one()
        quantity = self.quantity * line.qty_done
        if picking_id:
            line_vals = {
                "picking_id": picking_id.id,
                "product_id": self.product_id.id or False,
                "pack_parent_line_id": line.id,
                "pack_depth": line.pack_depth + 1,
                "company_id": picking_id.company_id.id,
                "location_id": picking_id.location_id.id,
                "location_dest_id": picking_id.location_dest_id.id,
                "pack_modifiable": line.product_id.pack_modifiable,
            }
            pol = line.new(line_vals)
            pol._onchange_product_id()
            pol.qty_done = quantity
            pol._onchange_qty_done()
            vals = pol._convert_to_write(pol._cache)
            return vals
        else:
            line_vals = {
                # "picking_id": self.picking_id.id,
                "product_id": self.product_id.id or False,
                "pack_parent_line_id": line.id,
                "pack_depth": line.pack_depth + 1,
                "company_id":line.company_id.id,
                "location_id": line.location_id.id,
                "location_dest_id": line.location_dest_id.id,
                "pack_modifiable": line.product_id.pack_modifiable,
            }
            pol = line.new(line_vals)
            pol._onchange_product_id()
            pol.qty_done = quantity
            pol._onchange_qty_done()
            vals = pol._convert_to_write(pol._cache)
            return vals
        # line_vals = {
        #     "picking_id": picking_id.id,
        #     "product_id": self.product_id.id or False,
        #     "pack_parent_line_id": line.id,
        #     "pack_depth": line.pack_depth + 1,
        #     "company_id": picking_id.company_id.id,
        #     "location_id": picking_id.location_id.id,
        #     "location_dest_id": picking_id.location_dest_id.id,
        #     "pack_modifiable": line.product_id.pack_modifiable,
        # }
        # pol = line.new(line_vals)
        # pol._onchange_product_id()
        # pol.qty_done = quantity
        # pol._onchange_qty_done()
        # vals = pol._convert_to_write(pol._cache)
        # return vals

