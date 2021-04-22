# encoding: utf-8
# Part of Odoo - CLuedoo Edition. Ask Falinwa / CLuedoo representative for full copyright And licensing details.
{
    'name': 'Sale Project Extension',
    "version": '14.1.0.0.0',
    'license': 'OPL-1',
    'summary': 'Project for final customer Level 1',
    'sequence': 100,
    'category': 'Project',
    'author': 'CLuedoo',
    'website': 'https://www.cluedoo.com',
    'support': 'cluedoo@falinwa.com',
    "description": """

    """,
    'depends': [
        'sale_project',
        'fal_project_template_including_scheduled_activity',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/product_view.xml',
        'wizard/sale_project_wizard_view.xml',
    ],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
