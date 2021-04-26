# -*- coding: utf-8 -*-
{
    'name': "Connect Task with Meeting",
    'version': '14.0.2.0.0',
    'license': 'OPL-1',
    'summary': "Link Task with Meeting",
    'sequence': 0,
    'category': 'Tools',
    'author': "CLuedoo",
    'website': "https://www.cluedoo.com",
    'support': 'cluedoo@falinwa.com',
    'description': "Enrich Feature to Link Task with Planning and Meeting",
    'depends': ['calendar', 'project', 'planning', 'industry_fsm'],
    # always loaded
    'data': [
        'views/project_task_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'css': [],
    'js': [],
    'qweb': [],
    'price': 0.00,
    'currency': 'EUR',
    'installable': True,
    'application': False,
    'auto_install': False,
}
