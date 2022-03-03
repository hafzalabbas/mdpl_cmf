odoo.define('custom_pos_receipt.model', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var rpc = require('web.rpc');

    models.load_fields('product.product', [
        'box_product'
    ]);

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function() {
            var line = _super_orderline.export_for_printing.apply(this,arguments);
            line.product_id = this.get_product().id;
            line.box_product = this.get_product().box_product;
            return line;
        },
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({

        initialize: function(attributes,options){
            this.customer_box_details = null;
            _super_order.initialize.apply(this,arguments);
        },
        get_onhand_box_details: function() {
            return this.customer_box_details;
        },
        get_current_order_box_details: function(){
            var pack_product = {};
            var full_details = [];
            var self = this;
            var orderlines = this.get_orderlines();
            for(var i = 0; i < orderlines.length; i++){

                if(orderlines[i].product.box_product == true){
                    pack_product[orderlines[i].product.id] = (pack_product[orderlines[i].product.id] || 0) + orderlines[i].quantity;
                }
            }
            if (pack_product){
                return pack_product;
            }
            else{
                return null;
            }
        },
        export_for_printing: function(){
            var json = _super_order.export_for_printing.apply(this,arguments);
            if (this.get_client()) {
                json.box_details = this.get_onhand_box_details();
            }
            return json;
        },
    });

});