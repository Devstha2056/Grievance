import re

from odoo import _, api, fields, models
from odoo.exceptions import UserError


def _build_code_from_name(name):
    code = re.sub(r'[^a-z0-9]+', '_', (name or '').strip().lower()).strip('_')
    return code or 'item'


class GrievanceResolutionOutcome(models.Model):
    _name = 'employee.grievance.resolution.outcome'
    _description = 'Grievance Resolution Outcome'
    _order = 'sequence, name'

    name = fields.Char(string='Outcome', required=True)
    code = fields.Char(string='Code', required=True, index=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code') and vals.get('name'):
                vals['code'] = _build_code_from_name(vals['name'])
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('name') and not vals.get('code'):
            vals['code'] = _build_code_from_name(vals['name'])
        return super().write(vals)


class GrievanceDisciplinaryAction(models.Model):
    _name = 'employee.grievance.disciplinary.action'
    _description = 'Grievance Disciplinary Action'
    _order = 'sequence, name'

    name = fields.Char(string='Disciplinary Action', required=True)
    code = fields.Char(string='Code', required=True, index=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code') and vals.get('name'):
                vals['code'] = _build_code_from_name(vals['name'])
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('name') and not vals.get('code'):
            vals['code'] = _build_code_from_name(vals['name'])
        return super().write(vals)


class GrievanceTicket(models.Model):
    _name = 'employee.grievance'
    _description = 'Grievance Ticket'
    _rec_name = 'name'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', readonly=True, copy=False, default='New')
    is_anonymous = fields.Boolean(string='Is Anonymous', default=False)
    incident_date = fields.Datetime(string='Incident Date')
    incident_location = fields.Char(string='Incident Location')
    grievance_type = fields.Many2one('employee.grievance.type', string='Grievance Type')
    confidential_note = fields.Text(string='Confidential Notes', help='Internal confidential notes for the ticket')
    investigation_notes = fields.Text(string='Investigation Notes', help='Details about the investigation process for this grievance.')
    interview_notes = fields.Text(string='Interview Notes', help='Notes recorded during interviews related to this grievance.')
    interview_document_ids = fields.Many2many(
        'ir.attachment',
        'grievance_interview_doc_rel',
        'grievance_id',
        'attachment_id',
        string='Interview Documents',
    )
    rejection_reason = fields.Text(string='Rejection Reason', help='Reason for rejecting this grievance.')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Priority', default='medium', help='Set the priority level of the grievance.')
    confidentiality_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('strict', 'Strict'),
    ], string='Confidentiality Level', default='low', help='Set the confidentiality level for this grievance.')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('acknowledged', 'Acknowledged'),
        ('assigned', 'Assigned'),
        ('investigation', 'Investigation'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        default=lambda self: self.env.user.employee_id,
        help='Employee who reported the ticket',
        readonly=True,
    )
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id', store=True, readonly=True)
    assigned_to = fields.Many2many(
        'hr.employee',
        'grievance_assignee_rel',
        'grievance_id',
        'employee_id',
        string='Assigned To',
        help='HR officers responsible for handling this grievance.',
        tracking=True,
    )
    persons_involved_ids = fields.Many2many(
        'hr.employee',
        'grievance_persons_involved_rel',
        'grievance_id',
        'employee_id',
        string='Persons Involved',
        help='Employees directly involved in or related to this grievance.',
    )
    deadline = fields.Date(string='Deadline', help='Expected date to resolve this grievance.')
    investigation_document_ids = fields.Many2many(
        'ir.attachment',
        'grievance_investigation_doc_rel',
        'grievance_id',
        'attachment_id',
        string='Investigation Documents',
    )
    supporting_evidence_ids = fields.Many2many(
        'ir.attachment',
        'grievance_supporting_evidence_rel',
        'grievance_id',
        'attachment_id',
        string='Supporting Evidence',
    )
    resolution_date = fields.Datetime(string='Resolution Date', readonly=True, help='Date and time when the grievance was resolved.')
    planned_activity_ids = fields.One2many(
        'mail.activity',
        'res_id',
        string='Planned Activities',
        domain=lambda self: [('res_model', '=', self._name), ('date_done', '=', False)],
    )
    interview_log_ids = fields.One2many('employee.grievance.interview.log', 'grievance_id', string='Interview Records')
    resolution_outcome_id = fields.Many2one('employee.grievance.resolution.outcome', string='Outcome', tracking=True)
    resolution_description = fields.Text(string='Resolution Description', help='Detailed description of how the grievance was resolved.')
    disciplinary_action_id = fields.Many2one('employee.grievance.disciplinary.action', string='Disciplinary Action')
    corrective_actions = fields.Text(string='Corrective Actions Required', help='List of corrective actions to be taken.')
    investigating_officer_id = fields.Many2one('hr.employee', string='Investigating Officer', help='Officer who conducted the investigation.')
    officer_signature = fields.Binary(string='Officer Signature', attachment=True)
    officer_signed_date = fields.Datetime(string='Officer Signed Date', readonly=True)
    hr_manager_approval_id = fields.Many2one('hr.employee', string='HR Manager', help='HR Manager approving the resolution.')
    hr_manager_signature = fields.Binary(string='HR Manager Signature', attachment=True)
    hr_manager_signed_date = fields.Datetime(string='HR Manager Signed Date', readonly=True)
    approval_state = fields.Selection([
        ('pending', 'Pending'),
        ('officer_signed', 'Officer Signed'),
        ('approved', 'Approved'),
    ], string='Approval Status', default='pending', tracking=True)
    notification_method = fields.Selection([
        ('secure_email', 'Secure Email (Anonymous Protected)'),
        ('direct_email', 'Direct Email'),
        ('letter', 'Physical Letter'),
        ('in_person', 'In Person'),
    ], string='Notification Method')
    complainant_message = fields.Text(string='Message to Complainant', help='Message to be sent to the complainant about the resolution.')
    complainant_notified = fields.Boolean(string='Complainant Notified', default=False)

    def init(self):
                self.env.cr.execute(
                        """
                        SELECT column_name
                            FROM information_schema.columns
                         WHERE table_name = 'employee_grievance'
                             AND column_name IN ('resolution_outcome', 'disciplinary_action')
                        """
                )
                existing_columns = {row[0] for row in self.env.cr.fetchall()}

                if 'resolution_outcome' in existing_columns:
                        self.env.cr.execute("""
                                UPDATE employee_grievance grievance
                                     SET resolution_outcome_id = outcome.id
                                    FROM employee_grievance_resolution_outcome outcome
                                 WHERE grievance.resolution_outcome_id IS NULL
                                     AND grievance.resolution_outcome = outcome.code
                        """)

                if 'disciplinary_action' in existing_columns:
                        self.env.cr.execute("""
                                UPDATE employee_grievance grievance
                                     SET disciplinary_action_id = action.id
                                    FROM employee_grievance_disciplinary_action action
                                 WHERE grievance.disciplinary_action_id IS NULL
                                     AND grievance.disciplinary_action = action.code
                        """)

    def action_submit(self):
        for record in self:
            record.state = 'submitted'
            record.message_post(body=_("Grievance submitted and pending acknowledgement."))

    def action_acknowledge(self):
        for record in self:
            record.state = 'acknowledged'
            record.message_post(body=_("Grievance acknowledged by HR."))

    def action_assign(self):
        for record in self:
            if not record.assigned_to:
                raise UserError(_("Please set the 'Assigned To' field before proceeding."))
            record.state = 'assigned'
            names = ', '.join(record.assigned_to.mapped('name'))
            record.message_post(body=_("Grievance assigned to %s.") % names)

    def action_reassign(self):
        for record in self:
            if not record.assigned_to:
                raise UserError(_("Please set the 'Assigned To' field before reassigning."))
            names = ', '.join(record.assigned_to.mapped('name'))
            record.message_post(body=_("Grievance reassigned to %s.") % names)

    def action_investigate(self):
        for record in self:
            record.state = 'investigation'
            record.message_post(body=_("Investigation has been started."))

    def action_resolve(self):
        for record in self:
            record.state = 'resolved'
            record.resolution_date = fields.Datetime.now()
            record.message_post(body=_("Grievance has been marked as resolved."))

    def action_officer_sign(self):
        for record in self:
            if not record.investigating_officer_id:
                raise UserError(_("Please set the Investigating Officer before signing."))
            if not record.officer_signature:
                raise UserError(_("Please add the investigating officer signature before signing."))
            record.officer_signed_date = fields.Datetime.now()
            record.approval_state = 'officer_signed'
            record.message_post(body=_("%s signed as Investigating Officer on %s.") % (
                record.investigating_officer_id.name,
                fields.Datetime.now().strftime('%B %d, %Y – %I:%M %p')
            ))

    def action_hr_manager_approve(self):
        for record in self:
            if not record.hr_manager_approval_id:
                raise UserError(_("Please set the HR Manager before approving."))
            if record.approval_state != 'officer_signed':
                raise UserError(_("Investigating Officer must sign before HR Manager approval."))
            if not record.hr_manager_signature:
                raise UserError(_("Please add the HR manager signature before approving."))
            record.hr_manager_signed_date = fields.Datetime.now()
            record.approval_state = 'approved'
            record.message_post(body=_("%s approved the resolution on %s.") % (
                record.hr_manager_approval_id.name,
                fields.Datetime.now().strftime('%B %d, %Y – %I:%M %p')
            ))

    def action_notify_complainant(self):
        for record in self:
            record.complainant_notified = True
            record.message_post(body=_("%s notified via %s.") % (
                record.employee_id.name or 'Complainant',
                dict(record._fields['notification_method'].selection).get(record.notification_method, 'N/A')
            ))

    def action_close(self):
        for record in self:
            record.state = 'closed'
            record.message_post(body=_("Grievance ticket has been closed."))

    def action_reject(self):
        for record in self:
            record.state = 'rejected'
            record.message_post(body=_("Grievance has been rejected."))

    def action_reset_draft(self):
        for record in self:
            record.state = 'draft'
            record.message_post(body=_("Grievance has been reset to draft."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('employee.grievance') or 'New'
        records = super().create(vals_list)
        for record in records:
            self.env['ir.logging'].create({
                'name': 'Grievance Created',
                'type': 'server',
                'dbname': self.env.cr.dbname,
                'level': 'info',
                'message': f"Grievance {record.name} ({record.id}) created.",
                'path': 'grievance',
                'func': 'create',
                'line': 0,
            })
        return records

    def write(self, vals):
        result = super().write(vals)
        for record in self:
            self.env['ir.logging'].create({
                'name': 'Grievance Updated',
                'type': 'server',
                'dbname': self.env.cr.dbname,
                'level': 'info',
                'message': f"Grievance {record.name} ({record.id}) updated with {vals}.",
                'path': 'grievance',
                'func': 'write',
                'line': 0,
            })
        return result