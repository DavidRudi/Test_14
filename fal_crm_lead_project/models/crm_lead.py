import logging
from odoo import models, api, _, fields

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    fal_number_project = fields.Integer(
        compute='fal_count_project', string="Number of Project")
    # fal_analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    # fal_project_id = fields.Many2one('project.project', string="Project")

    def fal_count_project(self):
        res = []
        projects = self.env['project.project'].search([('crm_lead_id', '=', self.id)])
        for project in projects:
            res.append(project.id)
        self.fal_number_project = len(res)
        return {
            'name': _('Project'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.project',
            'views': [(self.env.ref('fal_crm_lead_project.view_project_fal_crm_lead_project').id or False, 'tree'), (self.env.ref('project.edit_project').id or False, 'form')],
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', res)],
        }

    # def _create_analytic_account(self):
    #     for lead in self:
    #         analytic_account = self.env['account.analytic.account'].create({
    #             'name': lead.name,
    #             'company_id': lead.company_id.id,
    #             'partner_id': lead.partner_id and lead.partner_id.id or False,
    #             'active': True,
    #         })
    #         lead.write({'fal_analytic_account_id': analytic_account.id})

    def timesheet_create_project(self):
        """ Generate project for the given lead, and link it.
            :param project: record of project.project in which the task should be created
            :return task: record of the created task
        """
        return {
            'name': _('Create Project'),
            'res_model': 'crm.lead.project',
            'view_mode': 'form',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': self.env.context,
        }
