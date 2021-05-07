# -*- coding: utf-8 -*-
# Part of Odoo - Cluedoo Edition. ask Falinwa / Cluedoo representative for full copyright and licensing details.
{
    "name": "Structured Payment Communication",
    'version': '14.0.1.0.0',
    'license': 'OPL-1',
    'summary': 'Delivery on report invoice',
    'category': 'Invoicing Management',
    'author': "CLuedoo",
    'website': "https://www.cluedoo.com",
    'support': 'cluedoo@falinwa.com',
    "description": """
        Structured Payment Communication
    """,
    'data': [
        'views/account_journal_views.xml'
    ],
    'depends' :[
        'account',
    ],
    'images': [
        'static/description/bank_provision_screenshoot.png'
    ],
    'demo': [
    ],
    'price': 0.00,
    'currency': 'EUR',
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
