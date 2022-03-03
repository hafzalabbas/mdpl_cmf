
from odoo import fields, models


class ProductPack(models.Model):
    _inherit = "product.pack.line"

    def get_purchase_order_line_vals(self, line, order):
        self.ensure_one()
        quantity = self.quantity * line.product_uom_qty
        line_vals = {
            "order_id": order.id,
            "product_id": self.product_id.id or False,
            "pack_parent_line_id": line.id,
            "pack_depth": line.pack_depth + 1,
            "company_id": order.company_id.id,
            "pack_modifiable": line.product_id.pack_modifiable,
        }
        pol = line.new(line_vals)
        pol.onchange_product_id()
        pol.onchange_product_id_warning()
        pol.product_qty = quantity
        pol._onchange_quantity()
        vals = pol._convert_to_write(pol._cache)
        pack_price_types = {"totalized", "ignored"}
        if line.product_id.pack_component_price == "detailed":
            vals["price_unit"] = self.offer_price
        elif (
            line.product_id.pack_type == "detailed"
            and line.product_id.pack_component_price in pack_price_types
        ):
            vals["price_unit"] = 0.0
        vals.update(
            {
                "name": "{}{}".format("> " * (line.pack_depth + 1), pol.name),
            }
        )
        return vals

