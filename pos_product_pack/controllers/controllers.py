# -*- coding: utf-8 -*-
# from odoo import http


# class PosProductPack(http.Controller):
#     @http.route('/pos_product_pack/pos_product_pack/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_product_pack/pos_product_pack/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_product_pack.listing', {
#             'root': '/pos_product_pack/pos_product_pack',
#             'objects': http.request.env['pos_product_pack.pos_product_pack'].search([]),
#         })

#     @http.route('/pos_product_pack/pos_product_pack/objects/<model("pos_product_pack.pos_product_pack"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_product_pack.object', {
#             'object': obj
#         })
