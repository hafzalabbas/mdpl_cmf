odoo.define("customer_credit_limit.pos", function (require) {
    "use strict";

    var models = require("point_of_sale.models");
    var core = require("web.core");
    var utils = require("web.utils");
    var rpc = require("web.rpc");

    var _t = core._t;
    var round_pr = utils.round_precision;

    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const ClientListScreen = require("point_of_sale.ClientListScreen");
    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");




    const MyPaymentScreen = (_PaymentScreen) =>
        class extends _PaymentScreen {




            async validateOrder(isForceValidate) {
                var currentOrder = this.currentOrder;
                var zero_paymentlines = _.filter(
                    currentOrder.get_paymentlines(),
                    function (p) {
                        return p.amount === 0;
                    }
                );
                _.each(zero_paymentlines, function (p) {
                    currentOrder.remove_paymentline(p);
                });
                var isDebt = currentOrder.updates_debt();
                var debt_amount = currentOrder.get_debt_delta();
                var client = currentOrder.get_client();
                if (client) {
                    currentOrder.debt_before = client.debt;
                    currentOrder.debt_after = currentOrder.debt_before + debt_amount;
                } else {
                    currentOrder.debt_before = false;
                    currentOrder.debt_after = false;
                }

                var paymentlines_with_credits_via_discounts = currentOrder.has_paymentlines_with_credits_via_discounts();

                var exceeding_debts = this.exceeding_debts_check();
                if (client && currentOrder.debt_after >client.debt_limit) {
                    this.showPopup("ErrorPopup", {
                        title: _t("Max Debt exceeded"),
                        body: _t(
                            "You cannot sell products on credit journal to the customer because its max debt value will be exceeded."
                        ),
                    });
                    return;
                }

                var violations = this.debt_journal_restricted_categories_check();

                await super.validateOrder(isForceValidate);
            }

        };

    Registries.Component.extend(PaymentScreen, MyPaymentScreen);


});
