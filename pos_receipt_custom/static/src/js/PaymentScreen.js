odoo.define('custom_pos_receipt.PaymentScreen', function (require) {
    "use strict";

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const PosReceiptCustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            async validateOrder(isForceValidate) {
                var client = this.currentOrder.get_client();
                if (client) {
                    var current_order_box = this.currentOrder.get_current_order_box_details();
                    try {
                        let box_details = await this.rpc({
                            model: 'pos.order',
                            method: 'get_onhand_box_details',
                            args: [client, current_order_box],
                        });
                        this.currentOrder.customer_box_details = box_details;
                    }
                    catch (error) {
                        this.currentOrder.customer_box_details = null;
                    }
                }
                return super.validateOrder(...arguments);
            }
        };

    Registries.Component.extend(PaymentScreen, PosReceiptCustomPaymentScreen);

    return PaymentScreen;

});