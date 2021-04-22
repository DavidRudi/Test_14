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
        cls.partner_P = cls.env['res.partner'].create({
            'name': 'Valid L',
            'email': 'valid.l@agrolait.com'})
        cls.project_template_1 = cls.env['project.project'].with_context({'mail_create_nolog': True}).create({
            'name': 'Project Template New',
            'privacy_visibility': 'portal',
            'fal_is_template': True,
            'delay_count': 3,
            'partner_id': cls.partner_P.id})
        # Already-existing tasks in Pigs
        cls.task_1 = cls.env['project.task'].with_context({'mail_create_nolog': True}).create({
            'name': 'Template UserTask',
            'delay_count': 4,
            'project_id': cls.project_template_1.id})
        # })

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
        self.lead = self.env['crm.lead'].create(lead_data)
        self.lead.partner_id = parter_lead_p

        wizard_vals = {
            'name': "Project Crm",
            'project_template_id': self.project_template_1.id,
        }
        wizard_project = self.env['crm.lead.project'].create(wizard_vals)
        wizard_project.with_context({
            'active_id': self.lead.id}).action_create()
        self.assertEqual(self.lead.fal_number_project, 1)
