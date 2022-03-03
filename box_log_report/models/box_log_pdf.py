# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class ReportBoxLogPdf(models.AbstractModel):
    _name = "report.box_log_report.report_box_log_pdf"
    _description = "Box Log Report PDF"

    def get_box_details(self, data):
        company_id = data['company_id']
        partner_id = data['partner_id']
        range_type = data['type']
        report_type = data['report_type']
        date_from = data['date_from']
        date_to = data['date_to']
        box_details = []
        if report_type == 'purchase':
            if range_type == 'all':
                details = self.env['stock.move'].search(
                    [('picking_id.partner_id', '=', partner_id), ('company_id', '=', company_id),
                     ('product_id.box_product', '=', True), ('purchase_line_id', '!=', False),
                     ('state', '=', 'done')
                     ])
                if details:
                    for line in details:
                        box_info = {
                            'product': line.product_id.name,
                            'qty': line.quantity_done,
                            'date': line.date,
                            'order': line.purchase_line_id.order_id.name,
                            'status': 'Purchase' if line.to_refund is False or line.origin_returned_move_id is False else 'Return',
                        }
                        box_details.append(box_info)
            else:
                details = self.env['stock.move'].search([('picking_id.partner_id', '=', partner_id), ('company_id', '=', company_id),
                                               ('product_id.box_product', '=', True), ('purchase_line_id', '!=', False),
                                               ('date', '>=', date_from),
                                               ('date', '<=', date_to), ('state', '=', 'done')
                                               ])
                if details:
                    for line in details:
                        box_info = {
                            'product': line.product_id.name,
                            'qty': line.quantity_done,
                            'date': line.date,
                            'order': line.purchase_line_id.order_id.name,
                            'status': 'Purchase' if line.to_refund is False or line.origin_returned_move_id is False else 'Return',
                        }
                        box_details.append(box_info)
        else:
            if range_type == 'all':
                details = self.env['stock.move'].search(
                    [('picking_id.partner_id', '=', partner_id), ('company_id', '=', company_id),
                     ('product_id.box_product', '=', True), ('sale_line_id', '!=', False), ('state', '=', 'done')
                     ])
                if details:
                    for line in details:
                        box_info = {
                            'product': line.product_id.name,
                            'qty': line.quantity_done,
                            'date': line.date,
                            'order': line.sale_line_id.order_id.name,
                            'status': 'Sale' if line.to_refund is False or line.origin_returned_move_id is False else 'Return',
                        }
                        box_details.append(box_info)
                pos_details = self.env['pos.order.line'].search([('order_id.partner_id', '=', partner_id),
                                                                 ('company_id', '=', company_id),
                                                                 ('product_id.box_product', '=', True)])
                if pos_details:
                    for line in pos_details:
                        box_info = {
                            'product': line.product_id.name,
                            'qty': line.qty if line.qty >= 0 else line.qty*-1,
                            'date': line.order_id.date_order,
                            'order': line.order_id.name,
                            'status': 'Sale' if line.qty >= 0 else 'Return',
                        }
                        box_details.append(box_info)
            else:
                details = self.env['stock.move'].search([('picking_id.partner_id', '=', partner_id), ('company_id', '=', company_id),
                                                         ('product_id.box_product', '=', True),
                                                         ('sale_line_id', '!=', False),
                                                         ('date', '>=', date_from),
                                                         ('date', '<=', date_to), ('state', '=', 'done')
                                                         ])
                if details:
                    for line in details:
                        box_info = {
                            'product': line.product_id.name,
                            'qty': line.quantity_done,
                            'date': line.date,
                            'order': line.sale_line_id.order_id.name,
                            'status': 'Sale' if line.to_refund is False or line.origin_returned_move_id is False else 'Return',
                        }
                        box_details.append(box_info)
                pos_details = self.env['pos.order.line'].search([('order_id.partner_id', '=', partner_id),
                                                             ('company_id', '=', company_id),
                                                             ('order_id.date_order', '>=', date_from),
                                                             ('order_id.date_order', '<=', date_to),
                                                             ('product_id.box_product', '=', True)])
                if pos_details:
                    for line in pos_details:
                        box_info = {
                            'product': line.product_id.name,
                            'qty': line.qty if line.qty >= 0 else line.qty*-1,
                            'date': line.order_id.date_order,
                            'order': line.order_id.name,
                            'status': 'Sale' if line.qty >= 0 else 'Return',
                        }
                        box_details.append(box_info)
        return box_details

    def get_grouped_box_details(self, data):
        company_id = data['company_id']
        partner_id = data['partner_id']
        range_type = data['type']
        report_type = data['report_type']
        date_from = data['date_from']
        date_to = data['date_to']
        box_details = []
        details = '''
                select pol.product_id as product_id,pt.name as product,sum(pol.qty) as qty from pos_order_line pol
                left join pos_order po
                on po.id = pol.order_id
                left join product_product as pp
                on pp.id = pol.product_id
                left join product_template as pt
                on pt.id = pp.product_tmpl_id
                where po.partner_id = %s and po.company_id = %s and pt.box_product =true
                group by pol.product_id,pt.id
            '''
        self._cr.execute(details, (partner_id, company_id))
        for res in self._cr.dictfetchall():

            box_info = {
                'product': res['product'],
                'qty': res['qty'],
            }
            box_details.append(box_info)

        return box_details

    def get_box_history(self, data):
        company_id = data['company_id']
        partner_id = data['partner_id']
        range_type = data['type']
        report_type = data['report_type']
        date_from = data['date_from']
        date_to = data['date_to']
        # date_str = '09-19-2018'
        # date_object = datetime.strptime(date_str, '%m-%d-%Y').date()
        # print(type(date_object))
        # print(date_object)
        date_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_obj = date_obj - timedelta(days=1)

        box_details = []
        if report_type == 'purchase':
            if range_type == 'all':
                details = '''
                    SELECT SUM(CASE WHEN (sm.to_refund = true or sm.origin_returned_move_id is not null) 
                    THEN (product_uom_qty) ELSE 0 END) AS po_return, pt.name AS product, sm.product_id AS product_id, 
                    SUM(CASE WHEN ((sm.to_refund = false or sm.to_refund is null) and sm.origin_returned_move_id is null) 
                    THEN (product_uom_qty) ELSE 0 END) AS po 
                    from stock_move as sm
                    left join stock_picking as sp
                    on sp.id = sm.picking_id
                    left join product_product as pp
                    on pp.id = sm.product_id
                    left join product_template as pt
                    on pt.id = pp.product_tmpl_id
                    where sm.company_id = %s and sp.partner_id = %s and pt.box_product =true and 
                    sm.purchase_line_id is not null and sm.state = 'done'
                    group by sm.product_id,pt.id
                '''
                self._cr.execute(details, (company_id, partner_id))
                for res in self._cr.dictfetchall():
                    box_info = {
                        'product': res['product'],
                        'tray_ob': 0,
                        'purchase': res['po'],
                        'total': res['po'],
                        'return': res['po_return'],
                        'net_balance': res['po'] - res['po_return']
                    }
                    box_details.append(box_info)
            else:
                details = '''
                    SELECT CASE WHEN t1.product_id is not null then t1.product_id else t2.product_id end,
                    CASE WHEN t1.product is not null then t1.product else t2.product end,
                    CASE WHEN t1.product is not null then t1.product else t2.product end,
                    CASE WHEN t2.product_qty is not null then t2.product_qty else 0 end as tray_ob,
                    CASE WHEN t1.po is not null then t1.po else 0 end as po,
                    CASE WHEN t1.po_return is not null then t1.po_return else 0 end as po_return
                    FROM(
                        SELECT SUM(CASE WHEN (sm.to_refund = true or sm.origin_returned_move_id is not null) 
                        THEN (product_uom_qty) ELSE 0 END) AS po_return, pt.name AS product, sm.product_id AS product_id, 
                        SUM(CASE WHEN ((sm.to_refund = false or sm.to_refund is null) and sm.origin_returned_move_id is null) 
                        THEN (product_uom_qty) ELSE 0 END) AS po 
                        from stock_move as sm
                        left join stock_picking as sp
                        on sp.id = sm.picking_id
                        left join product_product as pp
                        on pp.id = sm.product_id
                        left join product_template as pt
                        on pt.id = pp.product_tmpl_id
                        where sm.company_id = %s and sp.partner_id = %s and pt.box_product =true and 
                        sm.purchase_line_id is not null and sm.state = 'done' and CAST(sm.date as DATE) BETWEEN %s AND %s
                        group by sm.product_id,pt.id
                    ) as t1
                    FULL JOIN (
                        SELECT pt.name AS product, sm.product_id AS product_id, sum(CASE  WHEN 
                        (sm.to_refund = true or sm.origin_returned_move_id is not null) THEN (-1*product_uom_qty)
                        WHEN ((sm.to_refund = false or sm.to_refund is null) and sm.origin_returned_move_id is null) 
                        THEN (product_uom_qty) ELSE 0 END )AS product_qty  from stock_move as sm
                        left join stock_picking as sp
                        on sp.id = sm.picking_id
                        left join product_product as pp
                        on pp.id = sm.product_id
                        left join product_template as pt
                        on pt.id = pp.product_tmpl_id
                        where sm.company_id = %s and sp.partner_id = %s and pt.box_product =true and 
                        sm.purchase_line_id is not null and sm.state = 'done' and CAST(sm.date as DATE) <= %s 
                        group by sm.product_id, pt.id 
                    ) as t2
                    on t1.product_id = t2.product_id
                '''
                self._cr.execute(details, (company_id, partner_id, date_from, date_to, company_id, partner_id, date_obj))
                for res in self._cr.dictfetchall():
                    box_info = {
                        'product': res['product'],
                        'tray_ob': res['tray_ob'],
                        'purchase': res['po'],
                        'total': res['tray_ob'] + res['po'],
                        'return': res['po_return'],
                        'net_balance': res['tray_ob'] + res['po'] - res['po_return']
                    }
                    box_details.append(box_info)
        else:
            if range_type == 'all':
                details = '''
                    SELECT product_id,product,sum(so) as sale,sum(so_return) as return
                    FROM(
                        (SELECT sm.product_id AS product_id, pt.name AS product,
                        SUM(CASE WHEN ((sm.to_refund = false or sm.to_refund is null) and sm.origin_returned_move_id is null) 
                           THEN (product_uom_qty) ELSE 0 END) AS so,
                        SUM(CASE WHEN (sm.to_refund = true or sm.origin_returned_move_id is not null) 
                           THEN (product_uom_qty) ELSE 0 END) AS so_return 
                        from stock_move as sm
                        left join stock_picking as sp
                        on sp.id = sm.picking_id
                        left join product_product as pp
                        on pp.id = sm.product_id
                        left join product_template as pt
                        on pt.id = pp.product_tmpl_id
                        where sm.company_id = %s and sp.partner_id = %s and pt.box_product =true and 
                        sm.sale_line_id is not null and sm.state = 'done'
                        group by sm.product_id,pt.id) 
                    UNION
                        (select pol.product_id as product_id,pt.name as product,
                        SUM(CASE WHEN (pol.qty>=0) THEN (pol.qty) ELSE 0 END) AS so,
                        SUM(CASE WHEN (pol.qty<0) THEN (-1*pol.qty) ELSE 0 END) AS so_return
                        from pos_order_line pol
                        left join pos_order po
                        on po.id = pol.order_id
                        left join product_product as pp
                        on pp.id = pol.product_id
                        left join product_template as pt
                        on pt.id = pp.product_tmpl_id
                        where po.partner_id = %s and po.company_id = %s and pt.box_product =true
                        group by pol.product_id,pt.id) 
                    ) t1
                    group by t1.product_id, t1.product
                    order by t1.product
                '''
                self._cr.execute(details, (company_id, partner_id, partner_id, company_id))
                for res in self._cr.dictfetchall():
                    box_info = {
                        'product': res['product'],
                        'tray_ob': 0,
                        'sale': res['sale'],
                        'total': res['sale'],
                        'return': res['return'],
                        'net_balance': res['sale'] - res['return']
                    }
                    box_details.append(box_info)
            else:
                details = '''
                    SELECT CASE WHEN table1.product_id is not null then table1.product_id else table2.product_id end,
                    CASE WHEN table1.product is not null then table1.product else table2.product end,
                    CASE WHEN table2.product_qty is not null then table2.product_qty else 0 end as tray_ob,
                    CASE WHEN table1.sale is not null then table1.sale else 0 end as sale,
                    CASE WHEN table1.return is not null then table1.return else 0 end as return
                    FROM(
                        SELECT product_id,product,sum(so) as sale,sum(so_return) as return
                        FROM(
                            (SELECT sm.product_id AS product_id, pt.name AS product,
                            SUM(CASE WHEN ((sm.to_refund = false or sm.to_refund is null) and sm.origin_returned_move_id is null) 
                               THEN (product_uom_qty) ELSE 0 END) AS so,
                            SUM(CASE WHEN (sm.to_refund = true or sm.origin_returned_move_id is not null) 
                               THEN (product_uom_qty) ELSE 0 END) AS so_return 
                            from stock_move as sm
                            left join stock_picking as sp
                            on sp.id = sm.picking_id
                            left join product_product as pp
                            on pp.id = sm.product_id
                            left join product_template as pt
                            on pt.id = pp.product_tmpl_id
                            where sm.company_id = %s and sp.partner_id = %s and pt.box_product =true and 
                            sm.sale_line_id is not null and sm.state = 'done' and CAST(sm.date as DATE) BETWEEN %s AND %s 
                            group by sm.product_id,pt.id) 
                        UNION
                            (select pol.product_id as product_id,pt.name as product,
                            SUM(CASE WHEN (pol.qty>=0) THEN (pol.qty) ELSE 0 END) AS so,
                            SUM(CASE WHEN (pol.qty<0) THEN (-1*pol.qty) ELSE 0 END) AS so_return
                            from pos_order_line pol
                            left join pos_order po
                            on po.id = pol.order_id
                            left join product_product as pp
                            on pp.id = pol.product_id
                            left join product_template as pt
                            on pt.id = pp.product_tmpl_id
                            where po.partner_id = %s and po.company_id = %s and pt.box_product =true and CAST(po.date_order as DATE) BETWEEN %s AND %s
                            group by pol.product_id,pt.id) 
                            ) t1
                        group by t1.product_id, t1.product
                        order by t1.product)table1
                    FULL JOIN (
                        SELECT product_id,product,sum(product_qty) as product_qty
                        FROM(
                            (SELECT sm.product_id AS product_id, pt.name AS product,
                             sum(CASE  WHEN (sm.to_refund = true or sm.origin_returned_move_id is not null) THEN (-1*product_uom_qty)
                             WHEN ((sm.to_refund = false or sm.to_refund is null) and sm.origin_returned_move_id is null) 
                             THEN (product_uom_qty) ELSE 0 END )AS product_qty
                            from stock_move as sm
                            left join stock_picking as sp
                            on sp.id = sm.picking_id
                            left join product_product as pp
                            on pp.id = sm.product_id
                            left join product_template as pt
                            on pt.id = pp.product_tmpl_id
                            where sm.company_id = %s and sp.partner_id = %s and pt.box_product =true and 
                            sm.sale_line_id is not null and sm.state = 'done' and CAST(sm.date as DATE) <= %s
                            group by sm.product_id,pt.id) 
                        UNION
                            (select pol.product_id as product_id,pt.name as product,
                            sum(pol.qty)AS product_qty
                            from pos_order_line pol
                            left join pos_order po
                            on po.id = pol.order_id
                            left join product_product as pp
                            on pp.id = pol.product_id
                            left join product_template as pt
                            on pt.id = pp.product_tmpl_id
                            where po.partner_id = %s and po.company_id = %s and pt.box_product =true
                            and CAST(po.date_order as DATE) <= %s
                            group by pol.product_id,pt.id) 
                            ) t1
                        group by t1.product_id, t1.product
                        order by t1.product
                    ) table2
                    on table1.product_id = table2.product_id
               
                '''
                self._cr.execute(details, (company_id, partner_id, date_from, date_to, partner_id, company_id, date_from,
                                           date_to, company_id, partner_id, date_obj, partner_id, company_id, date_obj))
                for res in self._cr.dictfetchall():
                    box_info = {
                        'product': res['product'],
                        'tray_ob': res['tray_ob'],
                        'sale': res['sale'],
                        'total': res['tray_ob'] + res['sale'],
                        'return': res['return'],
                        'net_balance': res['tray_ob'] + res['sale'] - res['return']
                    }
                    box_details.append(box_info)
        return box_details

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        partner = self.env['res.partner'].browse(data['partner_id'])
        company = self.env['res.company'].browse(data['company_id'])
        box_log = self.get_box_details(data)
        # grouped_box_log = self.get_grouped_box_details(data)
        history = self.get_box_history(data)
        data.update({
            'partner': partner,
            'company': company,
            'box_log': box_log,
            # 'on_hand': grouped_box_log,
            'history': history
        })
        return data

