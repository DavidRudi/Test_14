from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    @api.onchange("analytic_account_id")
    def _onchange_reinvoice(self):
        if self.analytic_account_id:
            self.sale_order_id = False
