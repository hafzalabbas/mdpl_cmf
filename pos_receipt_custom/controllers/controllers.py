# -*- coding: utf-8 -*-
# from odoo import http


# class PosReceiptCustom(http.Controller):
#     @http.route('/pos_receipt_custom/pos_receipt_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_receipt_custom/pos_receipt_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_receipt_custom.listing', {
#             'root': '/pos_receipt_custom/pos_receipt_custom',
#             'objects': http.request.env['pos_receipt_custom.pos_receipt_custom'].search([]),
#         })

#     @http.route('/pos_receipt_custom/pos_receipt_custom/objects/<model("pos_receipt_custom.pos_receipt_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_receipt_custom.object', {
#             'object': obj
#         })
