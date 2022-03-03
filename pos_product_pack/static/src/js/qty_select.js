
odoo.define('pos_product_pack..pos_quantity_selector', function(require) {
    "use strict";
	const ProductItem = require('point_of_sale.ProductItem');
	const OrderWidget = require('point_of_sale.OrderWidget');
    const Registries = require('point_of_sale.Registries');
    var models = require('point_of_sale.models');
    var SuperOrder = models.Order.prototype;

    models.Order = models.Order.extend({
        initialize: function(attributes,options){
            this.option = options;
            this.wk_line_stock_qty = 0.0
            SuperOrder.initialize.call(this,attributes,options);
        },
        wk_render_product: function(){
            var self = this;
            var lines =self.get_orderlines();
            $('.product .fa.fa-plus-square').addClass('oe_hidden');
            $('.product .fa.fa-minus-square').addClass('oe_hidden');
            $('.product .product_qty_tag').addClass('oe_hidden');
            $('.product .product_qty_tag').text('0');
            $('.product').css({'box-shadow':''});
            lines.forEach(line => {
                var product = line.product;
                var product_sale_count = 0;
                var orderlines = self.get_orderlines();
                orderlines.forEach(element => {
                    if(element.product.id == product.id){
                        product_sale_count = product_sale_count + element.quantity
                    }
                });
                if(product_sale_count >0){
                    var product_elem ='.product[data-product-id=' +product.id+']'
                    $(product_elem + ' '+ '.fa.fa-plus-square').removeClass('oe_hidden');
                    $(product_elem + ' '+ '.fa.fa-minus-square').removeClass('oe_hidden');
                    $(product_elem + ' '+ '.product_qty_tag').removeClass('oe_hidden');
                    $(product_elem + ' '+ '.product_qty_tag').text(product_sale_count);
                    $(product_elem).css({'box-shadow':'0px 4px 15.36px 0.64px rgb(125, 202, 152), 0px 2px 6px 0px rgb(80, 217, 128)'});
                    $(product_elem + ' '+ '.product-img img').css({'max-width':'62px'});
                    $(product_elem + ' '+ '.product-name').css({'width':'81%'});
                }
                else{
                    var product_elem ='.product[data-product-id=' +product.id+']'
                    $(product_elem + ' '+ '.fa.fa-plus-square').addClass('oe_hidden');
                    $(product_elem + ' '+ '.fa.fa-minus-square').addClass('oe_hidden');
                    $(product_elem + ' '+ '.product_qty_tag').addClass('oe_hidden');
                    $(product_elem + ' '+ '.product_qty_tag').text('0');
                    $(product_elem).css({'box-shadow':''});
                    $(product_elem + ' '+ '.product-img img').css({'max-width':'120px'})
                    $(product_elem + ' '+ '.product-name').css({'width':'100%'});
                }

            });
        }
    });

	// Inherit ProductItem----------------
    const PosResProductItem = (ProductItem) =>
		class extends ProductItem {
            wk_remove_product(event) {
                var self = this;
                var order = self.env.pos.get_order();
                var product_id =$(event.target).attr('data-product-id')? $(event.target).attr('data-product-id'):$(event.target).closest('.product').attr('data-product-id');
                var orderline = _.find(order.get_orderlines(), function(line){ return line.product.id == product_id});
                if(orderline){
                    let quantity = orderline.quantity-2
                    if(quantity >0){
                        orderline.set_quantity(orderline.quantity-2, true);
                    }
                    else{
                        order.remove_orderline(orderline);
                        if(orderline.quantity == 1){
                            $(".input-button.numpad-backspace").click()
                            $(".input-button.numpad-backspace").click()
                        }
                        var is_orderline = _.find(order.get_orderlines(), function(line){
                            return line.product.id == product_id
                        });
                        if(is_orderline && is_orderline.quantity == 1){
                            order.remove_orderline(is_orderline);
                        }
                        else if(is_orderline){
                            let price = is_orderline.price;
                            is_orderline.set_quantity(is_orderline.quantity-1, true)
                            is_orderline.set_unit_price(price)
                        }
                    }
                }
            }
		};
    Registries.Component.extend(ProductItem, PosResProductItem);

    // Inherit OrderWidget----------------
    const PosResOrderWidget = (OrderWidget) =>
		class extends OrderWidget {
            _updateSummary() {
                super._updateSummary()
                this.env.pos.get_order().wk_render_product();
            }
		};
    Registries.Component.extend(OrderWidget, PosResOrderWidget);
});