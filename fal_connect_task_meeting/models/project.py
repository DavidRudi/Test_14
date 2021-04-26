from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class Task(models.Model):
    _inherit = "project.task"

    def action_create_planning(self):
        planning = self.env['planning.slot']
        fields_obj = self.env['ir.model.fields']
        model_obj = self.env['ir.model']
        planning_obj = model_obj.search([('model', '=', 'planning.slot')])
        task = fields_obj.search([('model_id', '=', planning_obj.id), ('name', '=', 'task_id')])
        project = fields_obj.search([('model_id', '=', planning_obj.id), ('name', '=', 'project_id')])
        for data in self:
            values = {
                'name': data.name,
                'employee_id': data.user_id.employee_id.id,
                'start_datetime': data.planned_date_begin,
                'end_datetime': data.planned_date_end,
                'role_id': False,
            }
        if task and project:
            values.update({
                'task_id': self.id,
                'project_id': self.project_id,
            })
        planning_created = planning.create(values)
        planning_created._compute_allocated_hours()
