# -*- coding: utf-8 -*-
# from odoo import http


# class BoxLogReport(http.Controller):
#     @http.route('/box_log_report/box_log_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/box_log_report/box_log_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('box_log_report.listing', {
#             'root': '/box_log_report/box_log_report',
#             'objects': http.request.env['box_log_report.box_log_report'].search([]),
#         })

#     @http.route('/box_log_report/box_log_report/objects/<model("box_log_report.box_log_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('box_log_report.object', {
#             'object': obj
#         })
