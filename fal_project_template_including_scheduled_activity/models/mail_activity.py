from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def _set_template(self):
        res_model = self._context.get('default_res_model')
        if res_model == 'project.task' and self._context.get('default_res_id'):
            default_res_id = self._context.get('default_res_id')
            project_task = self.env['project.task'].browse(default_res_id)
        return project_task.is_template

    @api.onchange('activity_type_id')
    def _onchange_activity_type_id(self):
        is_template = self._set_template()
        if self.activity_type_id:
            if self.activity_type_id.summary:
                self.summary = self.activity_type_id.summary
            self.date_deadline = self._calculate_date_deadline(self.activity_type_id)
            if is_template == True:
                self.user_id = self.env.ref('base.user_root')
            else:
                self.user_id = self.activity_type_id.default_user_id or self.env.user
            if self.activity_type_id.default_description:
                self.note = self.activity_type_id.default_description
            if is_template:
                self.is_template = True

    duration = fields.Integer(
        'Duration', default=0, required=True)
    assignment_logic = fields.Char(
        'Assignment Logic', help='Write python code to automatically assign responsible.')
    is_template = fields.Boolean(string="Is Template?", default=False, copy=False)
