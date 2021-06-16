# -*- coding: utf-8 -*-
{
    'name': "Snail Mail Lines",
    'version': '14.0.1.0.0',
    'license': 'OPL-1',
    'summary': """Add Snail Mail Lines in Snailmail letter""",
    'category': 'Tools',
    'author': "CLuedoo",
    'website': "https://www.cluedoo.com",
    'support': 'cluedoo@falinwa.com',

    'description': """
        This module is to manage snailmail
        Add Snailmail Lines
        Add Merge for Snailmail letter
    """,

    'depends': [
        'base',
        'snailmail_account',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/fal_snailmail.xml',
        'wizard/account_invoice_send_views.xml',
    ],
    # only loaded in demonstration mode
    "auto_install": False,
    "installable": True,
}