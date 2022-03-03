odoo.define('custom_pos_receipt.OrderReceipt', function(require) {
    'use strict';

    var core = require('web.core');
    var QWeb = core.qweb;
//    var rpc = require('web.rpc');
    const OrderReceipt = require('point_of_sale.OrderReceipt');
    const Registries = require('point_of_sale.Registries');

    const CustomPosReceiptOrderReceipt = OrderReceipt =>
        class extends OrderReceipt {

            get boxDetails() {
                var pack_product = {};
                var full_details = [];
                for (let line of this.orderlines) {

                    if(line.product.box_product == true){
                        pack_product[line.product.id] = (pack_product[line.product.id] || 0) + line.quantity;
                    }
                }

                for(var id in pack_product){
                    if(pack_product.hasOwnProperty(id)){
                        full_details.push(
                        {
                            product_id: id,
                            name: this.env.pos.db.product_by_id[id].display_name,
                            qty: pack_product[id],
                        });
                    }
                }
//                console.log(full_details);
                if (full_details.length != 0){
                    return full_details;
                }
                else{
                    return null;
                }
            }
//            get onHandBoxDetails() {
////                var client = this._receiptEnv.order.get_client();
////                if (!client) {
////                    return [];
////                }
////                let on_hand_box_Details = await this.rpc({
////                    model: 'pos.order',
////                    method: 'get_onhand_box_details',
////                    args: [client]
////                });
//                var box_details = this.receiptEnv.boxdetails;
//                return box_details;
//            }
//            get onHandBoxDetails() {
//                var client = this._receiptEnv.order.get_client();
//                if (!client) {
//                    return [];
//                }
//                var full_details = [];
////                let on_hand_box_Details = this.rpc({
////                    model: 'pos.order',
////                    method: 'get_onhand_box_details',
////                    args: [client]
////                });
////                console.log(on_hand_box_Details);
////                return on_hand_box_Details;
//                this.rpc({
//                    model: 'pos.order',
//                    method: 'get_onhand_box_details',
//                    args: [client]
//                }).then(function (result) {
////                    console.log(result);
////                    _.each(result, function (data) {
////                        full_details.push(data);
////                    });
////                    return full_details;
//                        this.on_hand_box_Details = result;
//                       return this.on_hand_box_Details;
//                });
////                var on_hand_box_Details = this._receiptEnv.order.get_onhand_box_details();
////                var contents = this.$el[0].querySelector('.wk-order-list-contents');
////                contents.innerHTML = "";
////                var on_hand_box_Details = 1;
////                let on_hand_box_Details = this.rpc({
////                    model: 'pos.order',
////                    method: 'get_on_hand_box_details',
////                    args: [[this._receiptEnv.order.id], client],
////                });
//
////                this.rpc({
////                    model: 'pos.order',
////                    method: 'get_on_hand_box_details',
////                    args: [[this._receiptEnv.order.id], client],
////                }).then(function (results) {
////                    contents.innerHTML = "";
////                    var orderline_html = QWeb.render('WkOrderLine', {
////				        customer_name:results,
////				    });
////				    var orderline = document.createElement('tbody');
////				    orderline.innerHTML = orderline_html;
////				    orderline = orderline.childNodes[1];
////				    contents.appendChild(orderline);
//////                    return results['name'];
//////                     _.each(results, function (data) {
//////                         var on_hand_box_Details  = data;
//////                     });
////                });
////
////                console.log(on_hand_box_Details);
////                if (on_hand_box_Details){
////                    return on_hand_box_Details;
////                }
////                else {
////                    return null;
////                }
//            }
        };

    Registries.Component.extend(OrderReceipt, CustomPosReceiptOrderReceipt);

    return OrderReceipt;
});