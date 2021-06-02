from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('cluedoo')
class TestSaleExpense(TransactionCase):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        cls.analytic_account_1 = cls.env['account.analytic.account'].create({
            'name': 'Test AA',
            'code': 'TESTSALE_REINVOICE',
            'company_id': cls.partner_a.company_id.id,
            'partner_id': cls.partner_a.id
        })

    def set_analytic_account(self):
        self.so = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'analytic_account_id': self.analytic_account_1.id,
            'order_line': [
                (0, 0, {
                    'name': self.company_data['product_delivery_cost'].id.name, 'product_id': self.company_data['product_delivery_cost'].id,
                    'product_uom_qty': 2, 'product_uom': self.company_data['product_delivery_cost'].uom_id.id,
                    'price_unit': self.company_data['product_delivery_cost'].id.list_price,
                }),
            ],
            'pricelist_id': self.env.ref('product.list0').id,
            'picking_policy': 'direct',
        })
        self.so.action_confirm()
        sheet = self.env['hr.expense.sheet'].create({
            'name': 'Expense for John Smith',
            'employee_id': self.expense_employee.id,
            'journal_id': self.company_data['default_journal_purchase'].id,
        })

        hr_expense = self.env['hr.expense'].create({
            'name': 'Air Travel',
            'product_id': self.company_data['product_delivery_cost'].id,
            'analytic_account_id': self.analytic_account_1.id,
            'unit_amount': 621.54,
            'employee_id': self.expense_employee.id,
            'sheet_id': sheet.id,
        })

        sale_order_ids = self.env['sale.order'].search([('analytic_account_id', '=', self.analytic_account_1.id)])
        hr_expense.write({'sale_order_id': sale_order_ids[0].id})

        self.assertEqual(sale_order_ids[0].analytic_account_1, self.analytic_account_1)
