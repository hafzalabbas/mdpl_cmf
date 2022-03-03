# -*- coding: utf-8 -*-
{
    'name': "POS Automatic Invoice",

    'summary': """

    The module will convert all the POS orders to Invoices automatically. 

        """,

    'description': """

     This Module allows to all POS order invoicing in Odoo  for Scheduled
        Actions / Cron jobs running in backend server


    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Point Of Sale',
    'version': "14.0.1.0.0",
    'license': 'AGPL-3',
    'support': "support@loyalitsolutions.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/cron.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'images': ['static/description/banner.png'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}