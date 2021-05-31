# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.hr_expense.tests.common import TestExpenseCommon
from odoo.addons.sale.tests.common import TestSaleCommon
from odoo.tests import tagged
import logging

_logger = logging.getLogger(__name__)


@tagged('cluedoo')
class TestMarkupReInvoice(TestExpenseCommon, TestSaleCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        cls.analytic_account_markup = cls.env['account.analytic.account'].create({
            'name': 'Test AA Mark-Up',
            'code': 'TESTSALE_REINVOICE_Mark-Up',
            'mark_up': 10,
            'company_id': cls.partner_a.company_id.id,
            'partner_id': cls.partner_a.id
        })

        cls.sale_order_a = cls.env['sale.order'].with_context(mail_notrack=True, mail_create_nolog=True).create({
            'partner_id': cls.partner_a.id,
            'partner_invoice_id': cls.partner_a.id,
            'partner_shipping_id': cls.partner_a.id,
            'analytic_account_id': cls.analytic_account.id,
            'pricelist_id': cls.company_data['default_pricelist'].id,
        })

    def test_expenses_at_cost(self):
        """ Test vendor bill at cost for product based on ordered and delivered quantities. """
        # create SO line and confirm SO (with only one line)
        sale_order_line1 = self.env['sale.order.line'].create({
            'name': self.company_data['product_order_cost'].name,
            'product_id': self.company_data['product_order_cost'].id,
            'product_uom_qty': 2,
            'qty_delivered': 1,
            'product_uom': self.company_data['product_order_cost'].uom_id.id,
            'price_unit': self.company_data['product_order_cost'].list_price,
            'order_id': self.sale_order_a.id,
        })
        self.sale_order_a.action_confirm()
        # create expense
        hr_expense = self.env['hr.expense'].create({
            'name': self.company_data['product_order_cost'].name,
            'employee_id': self.expense_employee.id,
            'product_id': self.company_data['product_order_cost'].id,
            'sale_order_id': self.sale_order_a.id,
            'analytic_account_id': self.sale_order_a.analytic_account_id.id,
        })
        hr_expense_sheet = hr_expense.action_submit_expenses()
        print("SSSSSSSSSS")
        print(hr_expense_sheet)
        hr_expense_sheet.approve_expense_sheets()
        hr_expense_sheet.action_sheet_move_create()
