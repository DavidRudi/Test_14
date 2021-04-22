# -*- coding: utf-8 -*-
# Part of Odoo Falinwa Edition. See LICENSE file for full copyright and licensing details.
{
    'name': 'CRM: Opportunity to Project',
    'version': '14.1.0.0',
    'license': 'OPL-1',
    'summary': "Manually create project from opportunity",
    'category': 'CRM',
    'author': "CLuedoo",
    'website': "https://www.cluedoo.com",
    'support': 'cluedoo@falinwa.com',
    'description': '''
        This module has features:
        =============================

        1. Create project from Opportunity
    ''',
    'depends': [
        'sale_crm',
        'sale_timesheet',
        'fal_project_template_including_scheduled_activity',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'wizard/crm_lead_project.xml',
    ],
    'images': [
        'static/description/lead_project_screenshot.png'
    ],
    'demo': [
    ],
    'price': 180.00,
    'currency': 'EUR',
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
