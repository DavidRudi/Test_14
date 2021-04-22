# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
import logging

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = 'project.project'

    def _get_date(self):
        return fields.Datetime.today()

    project_template = fields.Many2one(
        'project.project', string='Template',
        domain=[('fal_is_template', '=', True)])
    start_date = fields.Date(string='Start Date', default=_get_date)
    date_end = fields.Date(string='Ending Date', index=True, copy=False)
    fal_is_template = fields.Boolean(string="Is Template?")
    delay_count = fields.Integer(
        'Duration(days)', default=0,
        help='Number of days/week/month before executing the action. It allows to plan the action deadline.')

    @api.onchange('project_template')
    def _onchange_fal_project_template_id(self):
        if self.project_template:
            self.date_end = self.start_date + relativedelta(days=self.delay_count)
            self.user_id = self.project_template.user_id.id
            self.privacy_visibility = self.project_template.privacy_visibility

    @api.model
    def create(self, vals):
        # create new projects by taking tasks from the project template
        project = super(Project, self).create(vals)
        if vals.get('project_template'):
            tasks = self.env['project.task']
            old_to_new_tasks = {}
            template = vals.get('project_template')
            project_template = self.env['project.project'].browse(template)
            task_template = []
            type_template = []
            # stages
            for types in project_template.type_ids:
                type_template.append(types.id)
            project.type_ids = [(6, 0, type_template)]
            # task
            for task in project_template.task_ids:
                defaults = self._map_tasks_default_valeus(task, project_template)
                if task.parent_id:
                    # set the parent to the duplicated task
                    defaults['parent_id'] = old_to_new_tasks.get(task.parent_id.id, False)
                new_task = task.copy(defaults)
                new_task.project_id = project.id
                new_task.stage_id = task.stage_id.id
                task_template.append(new_task.id)
        return project

    def write(self, vals):
        res = super(Project, self).write(vals)
        for project in self:
            if project.task_count <= 0:
                template = vals.get('project_template')
                project_template = self.env['project.project'].browse(template)
                task_template = []
                type_template = []
                # stages
                for types in project_template.type_ids:
                    type_template.append(types.id)
                # task
                for task in project_template.task_ids:
                    defaults = self._map_tasks_default_valeus(task, project_template)
                    if task.parent_id:
                        # set the parent to the duplicated task
                        defaults['parent_id'] = old_to_new_tasks.get(task.parent_id.id, False)
                    new_task = task.copy(defaults)
                    new_task.project_id = project.id
                    new_task.stage_id = task.stage_id.id
                    task_template.append(new_task.id)
        return res

    @api.model
    def _map_tasks_default_valeus(self, task, project):
        res = super(Project, self)._map_tasks_default_valeus(task, project)
        localdict = {
            **{
                'project': project,
                'task': task,
                'user': self.env['res.users'],
                'result': None,
            }
        }
        if task.assignment_logic:
            assignment_logic = self._compute_assignment_logic(task.assignment_logic, localdict)
        else:
            assignment_logic = self.env.user
        res.update({
            'date_deadline': fields.Datetime.now() + relativedelta(days=task.delay_count),
            'user_id': assignment_logic.id,
        })
        # copy activity
        if task.activity_ids:
            list_ids = []
            for act in task.activity_ids:
                activity = act.copy()
                if activity.assignment_logic:
                    assignment_logic = self._compute_assignment_logic(activity.assignment_logic, localdict)
                else:
                    assignment_logic = self.env.user
                activity.write({
                    'user_id': assignment_logic.id,
                    'date_deadline': fields.Datetime.now() + relativedelta(days=activity.duration),
                })
                list_ids.append(activity.id)
            res.update({
                'activity_ids': list_ids,
            })
        return res

    def _compute_assignment_logic(self, assignment_logic, localdict):
        try:
            safe_eval(assignment_logic, localdict, mode='exec', nocopy=True)
            return localdict['result']
        except Exception as e:
            raise UserError(_('Wrong python Code'))

    # Method if you are in template, to automatically duplicate and create a new project
    def take_template(self):
        project_vals = []
        for temp in self:
            project_vals += [{
                'name': _("%s (copy)") % (temp.name),
                'fal_is_template': False,
                'project_template': temp.id,
                'date_end': self.start_date + relativedelta(days=self.delay_count),
            }]
            project = self.env['project.project'].create(project_vals)

            return {
                'name': _('Project'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'project.project',
                'type': 'ir.actions.act_window',
                'res_id': project.id,
                'target': 'current',
                'context': dict(form_view_initial_mode='edit')
            }


class Task(models.Model):
    _inherit = "project.task"

    delay_count = fields.Integer(
        'Duration(days)', default=0, required=True)
    assignment_logic = fields.Char(
        'Assignment Logic',
        help='Write python code to automatically assign responsible.')
    is_template = fields.Boolean('Is Template', related='project_id.fal_is_template', copy=False, invisible=True)

    @api.onchange('planned_hours')
    def _onchange_date_deadline(self):
        if self.planned_hours:
            self.date_deadline = fields.Datetime.now() + timedelta(days=round(self.planned_hours / 8 ))
        else:
            self.date_deadline = fields.Datetime.now()
