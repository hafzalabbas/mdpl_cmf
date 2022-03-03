# -*- coding: utf-8 -*-
# from odoo import http


# class AutomaticInvoice(http.Controller):
#     @http.route('/automatic_invoice/automatic_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/automatic_invoice/automatic_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('automatic_invoice.listing', {
#             'root': '/automatic_invoice/automatic_invoice',
#             'objects': http.request.env['automatic_invoice.automatic_invoice'].search([]),
#         })

#     @http.route('/automatic_invoice/automatic_invoice/objects/<model("automatic_invoice.automatic_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('automatic_invoice.object', {
#             'object': obj
#         })
