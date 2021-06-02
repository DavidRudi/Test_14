# -*- coding: utf-8 -*-
{
    'name': "Sale Expense Extension.",
    'version': '14.1.1.0.0',
    'license': 'OPL-1',
    'summary': "Sale - Expense Extension.",
    'sequence': 20,
    'category': 'Human Resource',
    'author': "CLuedoo",
    'website': "https://www.cluedoo.com",
    'support': 'cluedoo@falinwa.com',
    'description': """
        Domain Reinvoice based on Analytic Account.
    """,
    'depends': ['sale_expense'],
    'data': [
        'views/hr_expense_inherit_view.xml',
    ],
    'demo': [
    ],
    'application': False,
}
