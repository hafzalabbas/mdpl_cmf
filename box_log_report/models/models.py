# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BoxLogReportWizard(models.TransientModel):
    _name = "box.log.report.wizard"
    _description = "Box Log Report Wizard"

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id,
                                 required=True)
    report_type = fields.Selection([('sale', 'Sale'), ('purchase', 'Purchase')], string='Report', default='sale')
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    type = fields.Selection([('all', 'All'), ('range', 'Date Range')], 'Select', default='range')
    date_from = fields.Date(string='Date From', default=fields.Date.context_today)
    date_to = fields.Date(string='Date To', default=fields.Date.context_today)

    def print_report(self):
        data = {'date_from': self.date_from, 'date_to': self.date_to, 'partner_id': self.partner_id.id,
                'company_id': self.company_id.id, 'type': self.type, 'report_type': self.report_type}
        return self.env.ref('box_log_report.box_log_report_pdf').report_action([], data=data)

    # def export_pdf(self):
    #     self.ensure_one()
    #     context = self._context
    #     datas = {'ids': context.get('active_ids', [])}
    #     datas['model'] = 'account.move.line'
    #     datas['form'] = self.read()[0]
    #     for field in datas['form'].keys():
    #         if isinstance(datas['form'][field], tuple):
    #             datas['form'][field] = datas['form'][field][0]
    #
    #     return self.env.ref('statement_of_account_report.action_statement_of_account_pdf').report_action(self, data=datas)

    def export_xls(self):
        pass
    #     context = self._context
    #     datas = {'ids': context.get('active_ids', [])}
    #     datas['model'] = 'account.move.line'
    #     datas['form'] = self.read()[0]
    #     for field in datas['form'].keys():
    #         if isinstance(datas['form'][field], tuple):
    #             datas['form'][field] = datas['form'][field][0]
    #
    #     return self.env.ref('statement_of_account_report.action_statement_of_account_xls').report_action(self, data=datas)

