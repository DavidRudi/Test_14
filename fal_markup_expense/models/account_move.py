from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _sale_create_reinvoice_sale_line(self):
        res = super(AccountMoveLine, self)._sale_create_reinvoice_sale_line()
        for move_line in self:
            analytic_account = move_line.analytic_account_id
            for item in res:
                order_line = res[item]
                price_unit = order_line.price_unit
                _logger.info(price_unit)
                if move_line.product_id.expense_policy == 'sales_price' or 'cost':
                    _logger.info("XXXXXXXXXXX00")
                    if analytic_account.mark_up:
                        _logger.info(analytic_account.mark_up)
                        price_mark_up = move_line.product_id.standard_price * analytic_account.mark_up / 100
                        total_price = price_unit + price_mark_up
                        order_line.write({
                            'price_unit': total_price,
                        })
        return res
