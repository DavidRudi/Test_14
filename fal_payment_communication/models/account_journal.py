from odoo import fields, models, api, _
from odoo.exceptions import Warning
from odoo.tools.safe_eval import safe_eval

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    fal_python_code = fields.Text(string="Python Code")
    invoice_reference_type = fields.Selection(selection_add=[('python_code', 'Python Code')], ondelete={'python_code': 'set default'})


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_invoice_reference_odoo_python_code(self):
        self.ensure_one()
        reference_result = ''
        pycode = self.journal_id.fal_python_code
        if not pycode:
            return ''
        if pycode:
            localdict = {
            **{
                'move_id': self,
                'journal_id': self.journal_id,
                'payment_term_id': self.invoice_payment_term_id,
                'result': "",
            }
            }
            try:
                safe_eval(pycode, localdict, mode="exec", nocopy=True)
                reference_result = localdict['result']
            except Exception as e:
                warning = {}
                title = _("Warning for %s") % self.name
                message = e
                warning['title'] = title
                warning['message'] = message
                res = {'warning': warning}
            return reference_result
