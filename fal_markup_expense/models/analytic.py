from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class AccountAnalytic(models.Model):
    _inherit = 'account.analytic.account'

    mark_up = fields.Float('Mark-Up', help="Mark Up percentage for re-invoicing amount")
