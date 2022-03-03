odoo.define('pos_product_pack.pos_product_pack_file', function(require) {
	"use strict";

    var models = require('point_of_sale.models');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    var SuperOrderline = models.Orderline.prototype;

	models.load_models([
	 {
		model: 'product.pack.line',
		condition: function(self) {
			return true; },
		fields: ['id', 'parent_product_id', 'quantity', 'offer_price', 'product_id'],
		domain: function(self) {
			return []; },
		loaded: function(self, result) {
			self.set({ 'wk_pack_product': result });
		},
	}], { 'after': 'product.product' });

//
//	 var _super_order = models.Order.prototype;
//      models.Order = models.Order.extend({
//
//    add_product: function(product, options){
//      if(product.pack_ok==true){
//              var order = this;
////              var selected_orderline = order.get_selected_orderline();
//              var lines = order.orderlines.models;
//              var wk_pack_products = this.pos.get('wk_pack_product');
//              var flag = false;
//              if (selected_orderline){
//              if (selected_orderline.product.pack_ok==true){
//              if (selected_orderline.product.pack_line_ids)
//              {
//              for (var i = 0; i < selected_orderline.product.pack_line_ids.length; i++) {
//              for (var j = 0; j < lines.length; j++) {
//              for (var k = 0; k < wk_pack_products.length; k++) {
//               if (wk_pack_products[k].id == pack_product[i].pack_line_ids[j]) {
//
//              lines[i].set_quantity(quantity);
//              flag = true;
//              }
//              }
//
//              }
//
//              }
//
//                                               }
//                                           }}
//      }
//       _super_order.add_product.apply(this,arguments);
//
//    },
//    });



    const PosPackProductScreen = ProductScreen =>
        class extends ProductScreen {
            async _clickProduct(event) {
                let result = super._clickProduct(event);
                const product = event.detail;
                var pack_product = [];
                var had_pack = "";
                var packing=[];
                if (product.pack_ok == true) {
                    pack_product.push(product);
                    var wk_pack_products = this.env.pos.get('wk_pack_product');
                    for (var i = 0; i < pack_product.length; i++) {
                        if (pack_product[i].id == product.id && (pack_product[i].pack_line_ids).length > 0) {
                            for (var j = 0; j < (pack_product[i].pack_line_ids).length; j++) {
                                for (var k = 0; k < wk_pack_products.length; k++) {
                                    if (wk_pack_products[k].id == pack_product[i].pack_line_ids[j]) {
                                        packing.push(pack_product[i])
                                        had_pack = 1;

//                                           var order = this.env.pos.get_order();
//                                           var lines = order.orderlines.models;
//                                           var flag = false;
////                                           for (var i in lines){
//                                           if (wk_pack_products[k].id == pack_product[i].pack_line_ids[j]) {
////                                               if(lines[i].product.display_name == product.display_name){
//                                                   var qty = pack_product[i].get_quantity();
//                                                   lines[i].set_quantity(qty+1);
//                                                   flag = true;
//                                               }
////                                           }
//                                           if (!flag){
//                                               this.currentOrder.add_product(this.env.pos.db.product_by_id[wk_pack_products[k].product_id[0]],
//                                             {quantity: wk_pack_products[k].quantity,
//                                              price: wk_pack_products[k].offer_price,});
//                                           }
                                        this.currentOrder.add_product(this.env.pos.db.product_by_id[wk_pack_products[k].product_id[0]],
                                             {quantity: wk_pack_products[k].quantity,
                                              price: wk_pack_products[k].offer_price, merge:true,});
                                        var selected_orderline = this.currentOrder.get_selected_orderline();
                                        selected_orderline.price_manually_set = true;

//                                        selected_orderline.can_be_merged_with()
                                    }
                                }
                            }
                        }
                    }
                }


                return result
            }



            _setValue(val) {
            var num = 0;
            if (this.currentOrder.get_selected_orderline()){
                var num = this.currentOrder.get_selected_orderline().quantity;
            }

            let result = super._setValue(val);
            if (this.currentOrder.get_selected_orderline()) {
                if (this.state.numpadMode === 'quantity' && val !== 'remove') {
                    this.currentOrder.get_selected_orderline().set_quantity(val);
                    var product_lines = this.currentOrder.get_selected_orderline();
                    var orderline = this.currentOrder.get_orderlines();
                    var order = this.currentOrder;

                     if(product_lines){

                    if(product_lines.product.pack_ok==true){
//                        var lines = order.orderlines.models;
                      var wk_pack_products = this.env.pos.get('wk_pack_product');
                       if (product_lines.product.pack_line_ids){

                      for (var k = 0; k < wk_pack_products.length; k++) {
                      	for (var i = 0; i < product_lines.product.pack_line_ids.length; i++) {
                      for (var j = 0; j < orderline.length; j++) {
                       if (wk_pack_products[k].id == product_lines.product.pack_line_ids[i]) {
                       	if (orderline[j].product.id==wk_pack_products[k].product_id[0] && orderline[j].price==wk_pack_products[k].offer_price){
                        var new_val = (num-val)
                        new_val = Math.abs(new_val)
                        if (event.detail['key']==='Backspace'){
                        val = orderline[j].quantity-new_val
                        }
                        else
                        {
                        val = orderline[j].quantity+new_val
                        }

                      orderline[j].set_quantity(val);
//                       flag = true;
                       	}
                      }
                      }
                      }}}}}
                      }




            }
             return result
        }



        };
    Registries.Component.extend(ProductScreen, PosPackProductScreen);

    return ProductScreen;


});
