from odoo.addons.stock.tests.test_inventory import TestInventory
from odoo.tests import tagged


@tagged('cluedoo')
class PaymentCommunicationTest(TestInventory):
	
	def test_payment_communication(self):
		inventory = self.env['account.journal'].create(
			{
				'invoice_reference_type': 'python_code',
				'fal_python_code': 'result=1'
			})
		inventory.action_start()
		print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")

		# self.assertTrue(inventory.line_ids)
