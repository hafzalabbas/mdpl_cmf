odoo.define('pos_product_pack.pos_product_fields', function(require){
"use strict";

    var PosModels = require('point_of_sale.models');

    PosModels.load_fields('product.product', [
        'pack_line_ids','used_in_pack_line_ids','pack_ok'
    ]);
});
