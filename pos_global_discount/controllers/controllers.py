# -*- coding: utf-8 -*-
# from odoo import http


# class PosGlobalDiscount(http.Controller):
#     @http.route('/pos_global_discount/pos_global_discount/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_global_discount/pos_global_discount/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_global_discount.listing', {
#             'root': '/pos_global_discount/pos_global_discount',
#             'objects': http.request.env['pos_global_discount.pos_global_discount'].search([]),
#         })

#     @http.route('/pos_global_discount/pos_global_discount/objects/<model("pos_global_discount.pos_global_discount"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_global_discount.object', {
#             'object': obj
#         })
