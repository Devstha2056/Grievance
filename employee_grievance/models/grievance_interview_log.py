from odoo import fields, models


class GrievanceInterviewLog(models.Model):
    _name = 'employee.grievance.interview.log'
    _description = 'Grievance Interview Activity Log'
    _order = 'date_done desc'

    grievance_id = fields.Many2one(
        'employee.grievance',
        string='Grievance',
        ondelete='cascade',
        required=True,
    )
    activity_type_id = fields.Many2one('mail.activity.type', string='Activity Type')
    summary = fields.Char(string='Summary')
    user_id = fields.Many2one('res.users', string='Done By')
    date_done = fields.Datetime(string='Completed On')
    feedback = fields.Text(string='Feedback')


class MailActivityGrievanceLog(models.Model):
    _inherit = 'mail.activity'

    def action_feedback(self, feedback=False, attachment_ids=None):
        to_log = self.filtered(lambda activity: activity.res_model == 'employee.grievance' and activity.res_id)
        log_vals = [
            {
                'grievance_id': activity.res_id,
                'activity_type_id': activity.activity_type_id.id,
                'summary': activity.summary,
                'user_id': activity.user_id.id,
                'date_done': fields.Datetime.now(),
                'feedback': feedback or '',
            }
            for activity in to_log
        ]
        result = super().action_feedback(feedback=feedback, attachment_ids=attachment_ids)
        if log_vals:
            self.env['employee.grievance.interview.log'].create(log_vals)
        return result