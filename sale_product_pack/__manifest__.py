# -*- coding: utf-8 -*-
{
    'name': "Sale product Pack",

    'summary': """
        This module allows you to sale product packs""",

    'description': """
        This module allows you to sale product packs
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product_pack', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_pack_line_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/product_pack_line_demo.xml',
    ],
}
