# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = 'project.project'

    crm_count = fields.Integer(compute='compute_crm_count', string="Crm Count")
    crm_lead_id = fields.Many2one('crm.lead', 'Lead', domain="[('partner_id', '=', partner_id)]", readonly=True, copy=False, help="Lead to which the project is linked.")

    def compute_crm_count(self):
        res = []
        crm_count_datas = self.env['crm.lead'].search([('id', '=', self.crm_lead_id.id)])
        for count in crm_count_datas:
            res.append(count.id)
        self.crm_count = len(res)
        return {
            'name': _('Crm Lead'),
            'view_mode': 'tree,form',
            'res_model': 'crm.lead',
            'views': [(self.env.ref('crm.crm_case_tree_view_leads').id, 'tree'), (False, 'form')],
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', res)],
        }
