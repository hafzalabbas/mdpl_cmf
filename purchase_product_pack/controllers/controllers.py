# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseProductPack(http.Controller):
#     @http.route('/purchase_product_pack/purchase_product_pack/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_product_pack/purchase_product_pack/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_product_pack.listing', {
#             'root': '/purchase_product_pack/purchase_product_pack',
#             'objects': http.request.env['purchase_product_pack.purchase_product_pack'].search([]),
#         })

#     @http.route('/purchase_product_pack/purchase_product_pack/objects/<model("purchase_product_pack.purchase_product_pack"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_product_pack.object', {
#             'object': obj
#         })
