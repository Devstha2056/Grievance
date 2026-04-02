# -*- coding: utf-8 -*-

{
    'name': 'Employee Grievance',
    'version': '19.0.1.0.0',
    'summary': 'Standalone grievance management for employees and HR',
    'description': """
<section>
    <h2>Employee Grievance</h2>
    <p>
        Standalone grievance management for employees and HR teams, covering intake,
        assignment, investigation, interview tracking, approvals, and resolution follow-up.
    </p>
</section>
""",
    'category': 'Human Resources',
    'author': 'Custom',
    'license': 'LGPL-3',
    'depends': ['hr', 'mail'],
    'images': ['static/description/banner.png', 'static/description/thumbnail.png'],
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