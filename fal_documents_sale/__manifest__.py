# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Documents - Sale',
    'version': '14.1.0.0',
    'category': 'Productivity/Documents',
    'summary': 'Sale from documents',
    'description': """
Add the ability to create invoices from the document module.
""",
    'website': ' ',
    'depends': ['documents', 'sale'],
    'data': [
        'data/data.xml',
        'views/documents_views.xml'
    ],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}
