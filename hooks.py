# -*- coding: utf-8 -*-


GRIEVANCE_XML_IDS = (
    'access_employee_grievance',
    'access_employee_grievance_type',
    'access_employee_grievance_type_manager',
    'access_hr_grievance_policy_tag',
    'access_hr_grievance_policy_tag_manager',
    'access_grievance_interview_log',
    'access_grievance_interview_log_manager',
    'access_grievance_resolution_outcome_user',
    'access_grievance_resolution_outcome_manager',
    'access_grievance_disciplinary_action_user',
    'access_grievance_disciplinary_action_manager',
    'rule_grievance_own_employee',
    'rule_grievance_hr_manager_all',
    'seq_employee_grievance',
    'grievance_resolution_outcome_substantiated_action_taken',
    'grievance_resolution_outcome_substantiated_no_action',
    'grievance_resolution_outcome_unsubstantiated',
    'grievance_resolution_outcome_inconclusive',
    'grievance_resolution_outcome_withdrawn',
    'grievance_disciplinary_action_none',
    'grievance_disciplinary_action_verbal_warning',
    'grievance_disciplinary_action_written_warning',
    'grievance_disciplinary_action_suspension',
    'grievance_disciplinary_action_termination',
    'grievance_disciplinary_action_other',
    'grievance_ticket_list',
    'grievance_ticket_search',
    'grievance_ticket_kanban',
    'grievance_ticket_form',
    'action_grievance_ticket',
    'action_grievance_ticket_menu',
)


def pre_init_hook(env):
    env.cr.execute(
        """
        UPDATE ir_model_data
           SET module = 'employee_grievance'
         WHERE module = 'hrms_dashboard'
           AND name = ANY(%s)
        """,
        (list(GRIEVANCE_XML_IDS),),
    )