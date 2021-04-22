from odoo.addons.crm.tests.common import TestCrmCommon
from odoo.tests.common import Form, tagged


@tagged('cluedoo')
class TestCRMLeadProject(TestCrmCommon):
    @classmethod
    def setUpClass(cls):
        super(TestCRMLeadProject, cls).setUpClass()
        cls.country_ref = cls.env.ref('base.be')
        cls.test_email = '"Test Email" <test.email@example.com>'
        cls.test_phone = '0485112233'

    def test_crm_lead_creation_with_project(self):
        parter_lead_p = self.env['res.partner'].create({
            'name': 'Test partner',
            'is_company': True,
            'mobile': '123456789',
            'title': self.env.ref('base.res_partner_title_mister').id,
            'function': 'My function',
        })
        lead_data = {
            'name': 'Test with Project',
            'contact_name': 'Test',
            'street': 'My street',
            'country_id': self.country_ref.id,
            'email_from': self.test_email,
            'phone': self.test_phone,
            'mobile': '987654321',
            'website': 'http://mywebsite.test.org',
        }
        lead = self.env['crm.lead'].create(lead_data)
        lead.partner_id = parter_lead_p
        lead.timesheet_create_project()
        self.assertEqual(lead.fal_number_project, 1)
