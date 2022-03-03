odoo.define('customer_credit_limit.pos_product_fields', function(require){
"use strict";

    var PosModels = require('point_of_sale.models');

    PosModels.load_fields('res.partner', [
        'debt_limit'
    ]);
});
