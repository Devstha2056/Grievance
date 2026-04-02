from odoo import fields, models


class GrievanceType(models.Model):
    _name = 'employee.grievance.type'
    _description = 'Grievance Type'
    _order = 'name'

    name = fields.Char(string='Grievance Type', required=True)
    active = fields.Boolean(string='Active', default=True)