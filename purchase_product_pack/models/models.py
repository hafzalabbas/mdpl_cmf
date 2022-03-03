# -*- coding: utf-8 -*-

from odoo import _, api, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def copy(self, default=None):
        purchase_copy = super().copy(default)
        # we unlink pack lines that should not be copied
        pack_copied_lines = purchase_copy.order_line.filtered(
            lambda l: l.pack_parent_line_id.order_id == self
        )
        pack_copied_lines.unlink()
        return purchase_copy

    @api.onchange("order_line")
    def check_pack_line_unlink(self):
        """At least on embeded tree editable view odoo returns a recordset on
        _origin.order_line only when lines are unlinked and this is exactly
        what we need
        """
        origin_line_ids = self._origin.order_line.ids
        line_ids = self.order_line.ids
        removed_line_ids = list(set(origin_line_ids) - set(line_ids))
        removed_line = self.env["purchase.order.line"].browse(removed_line_ids)
        if removed_line.filtered(
            lambda x: x.pack_parent_line_id
            and not x.pack_parent_line_id.product_id.pack_modifiable
        ):
            raise UserError(
                _(
                    "You cannot delete this line because is part of a pack in"
                    " this purchase order. In order to delete this line you need to"
                    " delete the pack itself"
                )
            )

    def write(self, vals):
        if "order_line" in vals:
            to_delete_ids = [e[1] for e in vals["order_line"] if e[0] == 2]
            subpacks_to_delete_ids = (
                self.env["purchase.order.line"]
                .search(
                    [("id", "child_of", to_delete_ids), ("id", "not in", to_delete_ids)]
                )
                .ids
            )
            if subpacks_to_delete_ids:
                for cmd in vals["order_line"]:
                    if cmd[1] in subpacks_to_delete_ids:
                        if cmd[0] != 2:
                            cmd[0] = 2
                        subpacks_to_delete_ids.remove(cmd[1])
                for to_delete_id in subpacks_to_delete_ids:
                    vals["order_line"].append([2, to_delete_id, False])
        return super().write(vals)


