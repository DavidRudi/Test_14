import logging
from odoo import models, api, _, fields

_logger = logging.getLogger(__name__)


class CrmLeadProject(models.TransientModel):
    _name = 'crm.lead.project'

    @api.model
    def _get_crm(self):
        if self.env.context.get('active_id'):
            active_id = self.env.context.get('active_id')
            crm_lead = self.env['crm.lead'].browse(active_id)
            return crm_lead

    name = fields.Char(string='Name')
    fal_analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    crm_id = fields.Many2one('crm.lead', string="Crm Lead", default=_get_crm)
    project_template_id = fields.Many2one('project.project', string="Project Template", domain="[('fal_is_template', '=', True)]")

    @api.onchange('project_template_id')
    def _onchange_project_template(self):
        if self.project_template_id:
            if self.project_template_id.analytic_account_id:
                self.fal_analytic_account_id = self.project_template_id.analytic_account_id
            else:
                self.fal_analytic_account_id = False

    def action_create(self):
        # if self.env.context:
        project = self.env['project.project'].create({
            'name': self.name,
            'project_template': self.project_template_id.id,
            'analytic_account_id': self.fal_analytic_account_id.id,
            'crm_lead_id': self.crm_id.id,
        })
        return project
