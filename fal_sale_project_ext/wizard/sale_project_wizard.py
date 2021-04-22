import logging
from odoo import models, api, _, fields
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class SaleProjectWizard(models.TransientModel):
    _name = 'sale.project.wizard'

    @api.model
    def _get_sale_order(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            sale_order_id = self.env['sale.order'].browse(active_id)
            return sale_order_id

    @api.model
    def _get_project_template(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            sale_order_id = self.env['sale.order'].browse(active_id)
            for order in sale_order_id.order_line:
                project_template_id = sale_order_id.project_template_id or order[0].product_id.project_template_id
            return project_template_id

    @api.depends('sale_order_id', 'project_template_id')
    def get_analytic_account(self):
        if self.sale_order_id.analytic_account_id:
            self.fal_analytic_account_id = self.sale_order_id.analytic_account_id
        else:
            self.fal_analytic_account_id = self.project_template_id.analytic_account_id

    name = fields.Char(string='Name')
    fal_analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account", compute='get_analytic_account')
    sale_order_id = fields.Many2one('sale.order', string="Sale Order", default=_get_sale_order)
    project_template_id = fields.Many2one('project.project', string="Project Template", domain="[('fal_is_template', '=', True)]", default=_get_project_template)

    def action_create(self):
        delay_count = self.project_template_id.delay_count
        project = self.project_template_id.copy({
            'name': self.name,
            'partner_id': self.sale_order_id.partner_id.id,
            'project_template': self.project_template_id.id,
            'analytic_account_id': self.fal_analytic_account_id.id,
            'sale_order_id': self.sale_order_id.id,
            'company_id': self.sale_order_id.company_id.id,
            'fal_is_template': False,
            'date_end': fields.Datetime.now() + relativedelta(days=delay_count),
            'project_template': self.project_template_id.id,
        })
        self.sale_order_id.write({'project_id': project.id})
        return project
