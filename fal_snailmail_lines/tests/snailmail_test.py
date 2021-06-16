from odoo.addons.snailmail_account.tests.test_pingen_send import TestPingenSend
from odoo.tests import tagged
import logging

_logger = logging.getLogger(__name__)

@tagged('cluedoo')
class SnailmailLinesTest(TestPingenSend):
	def setUp(self):
		is_merge = True
		invoices = []
		for i in range(2):
			invoice = []
	        invoices.pingen_url = "https://stage-api.pingen.com/document/upload/token/30fc3947dbea4792eb12548b41ec8117/"
	        invoices.sample_invoice = self.create_invoice()
	        invoices.sample_invoice.partner_id.vat = "BE000000000"
        invoices.append(invoice)

        self.letter = self.env['account.invoice.send'].create({
        	'invoice_ids': invoices,
        	'is_merge': True,
        	'snailmail_is_letter': True,
        	'is_email': False,
        	'is_print': False,
        	})
        _logger.info(self.letter, "ppppppppppppp")


        self.send_and_print_action()


        