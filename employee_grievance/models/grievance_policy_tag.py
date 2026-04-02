from odoo import fields, models


class HrGrievancePolicyTag(models.Model):
    _name = 'hr.grievance.policy.tag'
    _description = 'Grievance Policy Violation Tag'
    _order = 'name'

    name = fields.Char(string='Policy Tag', required=True)
    color = fields.Integer(string='Color', default=0)