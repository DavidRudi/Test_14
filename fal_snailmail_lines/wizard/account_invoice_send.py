from odoo import models, api, fields, _
from odoo.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)


class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'

    is_merge = fields.Boolean('Merge',
        help='Allows to merge the document for Snailmail Letter',
        default=False)

    @api.depends('snailmail_is_letter')
    def _check_partner(self):
        for partner in self.activity_ids:
            if self.activity_ids.invoice_partner_display_name[0] != partner.invoice_partner_display_name:
                raise Warning(_("Customer name must be same"))

    @api.onchange('is_merge')
    def _compute_snailmail_cost(self):
        if self.is_merge: self.snailmail_cost = 1
        else:
            for wizard in self:
                wizard.snailmail_cost = len(wizard.invoice_ids.ids)


    @api.onchange('snailmail_is_letter')
    def _onchange_is_merge(self):
        if not self.snailmail_is_letter: self.is_merge = False

    def snailmail_print_action(self):
        self = self.with_context(is_merge = self.is_merge)
        res = super(AccountInvoiceSend, self).snailmail_print_action()
        multiple_partner=False
        temp=[]
        for invoice in self.invoice_ids:
            temp.append(invoice.invoice_partner_display_name)
        if len(set(temp)) != 1: multiple_partner = True

        if self.is_merge and multiple_partner:
            raise Warning(_('Cannot merge snailmail, there are more than one partner in selected invoice'))
        return res