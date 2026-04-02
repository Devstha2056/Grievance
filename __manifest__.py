# -*- coding: utf-8 -*-

{
    'name': 'Employee Grievance',
    'version': '19.0.1.0.0',
    'summary': 'Standalone grievance management for employees and HR',
    'description': 'Separates grievance management from the HRMS dashboard into its own addon.',
    'category': 'Human Resources',
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/grievance_rules.xml',
        'data/grievance_data.xml',
        'views/grievance_view.xml',
    ],
    'pre_init_hook': 'pre_init_hook',
    'installable': True,
    'application': False,
}