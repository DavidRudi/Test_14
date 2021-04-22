from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_template_id = fields.Many2one('project.project', 'Project Template', copy=False,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, domain="[('fal_is_template', '=', True)]")
    visible_project_template = fields.Boolean('Display project', compute='_compute_visible_project_template', readonly=True)

    @api.depends('order_line.product_id.service_tracking')
    def _compute_visible_project_template(self):
        for order in self:
            order.visible_project_template = any(
                service_tracking == 'task_in_project' or 'project_only' for service_tracking in order.order_line.mapped('product_id.service_tracking')
            )

    def create_project(self):
        return {
            'name': _('Create Project'),
            'res_model': 'sale.project.wizard',
            'view_mode': 'form',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': self.env.context,
        }

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)
        if template.project_template_id:
            self.project_template_id = template.project_template_id
        return super(SaleOrder, self).onchange_sale_order_template_id()

    # @api.onchange('project_template_id')
    # def _onchange_project_template(self):
    #     for order in self.order_line:
    #         if order.product_id.service_tracking == 'task_in_project':
    #             order.project_template_id = self.project_template_id


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    project_template_id = fields.Many2one('project.project', 'Project Template',
        copy=False, index=True, domain="[('fal_is_template', '=', True)]")

    def _timesheet_create_project_prepare_values(self):
        res = super(SaleOrderLine, self)._timesheet_create_project_prepare_values()
        if self.product_id.project_template_id:
            delay_count = self.product_id.project_template_id.delay_count
            res.update({
                'fal_is_template': False,
                'date_end': fields.Datetime.now() + relativedelta(days=delay_count),
                'project_template': self.product_id.project_template_id.id,
            })
        return res

    def _timesheet_create_project(self):
        values = self._timesheet_create_project_prepare_values()
        if self.order_id.project_template_id and not self.order_id.project_id or self.product_id.project_template_id:
            if self.order_id.project_template_id:
                values['name'] = "%s - %s" % (values['name'], self.order_id.project_template_id.name)
                project = self.order_id.project_template_id.create(values)
                delay_count = project.delay_count
                project.write({
                    'fal_is_template': False,
                    'date_end': fields.Datetime.now() + relativedelta(days=delay_count),
                })
                project.tasks.write({
                    'sale_line_id': self.id,
                    'partner_id': self.order_id.partner_id.id,
                    'email_from': self.order_id.partner_id.email,
                })
                # duplicating a project doesn't set the SO on sub-tasks
                project.tasks.filtered(lambda task: task.parent_id != False).write({
                    'sale_line_id': self.id,
                    'sale_order_id': self.order_id,
                })
            elif not self.order_id.project_template_id:
                project = super(SaleOrderLine, self)._timesheet_create_project()
        else:
            project = super(SaleOrderLine, self)._timesheet_create_project()

        if not project.type_ids:
            project.type_ids = self.env['project.task.type'].create({'name': _('New')})

        self.write({'project_id': project.id})
        return project


class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    visible_project = fields.Boolean('Display project', compute='_compute_visible_project', readonly=True)
    project_template_id = fields.Many2one('project.project', 'Project Template', copy=False, domain="[('fal_is_template', '=', True)]")

    @api.depends('sale_order_template_line_ids.product_id.service_tracking')
    def _compute_visible_project(self):
        for order in self:
            order.visible_project = any(
                service_tracking == 'task_in_project' for service_tracking in order.sale_order_template_line_ids.mapped('product_id.service_tracking')
            )
