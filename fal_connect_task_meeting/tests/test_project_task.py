from odoo.tests.common import TransactionCase
from odoo.addons.project.tests.test_project_base import TestProjectCommon
from odoo.tests import Form, tagged
from odoo.exceptions import UserError


@tagged('cluedoo')
class TestProjectTask(TestProjectCommon):
    @classmethod
    def setUpClass(cls):
        super(TestProjectTask, cls).setUpClass()

        cls.project_test = cls.env['project.project'].with_context({'mail_create_nolog': True}).create({
            'name': 'Connect To Meeting',
            'privacy_visibility': 'portal',
            'partner_id': False})
        # Already-existing tasks in Pigs
        cls.task_1 = cls.env['project.task'].with_context({'mail_create_nolog': True}).create({
            'name': 'Template UserTask',
            'user_id': cls.self.env.user,
            'planned_date_begin': "2021-04-07 11:00:00",
            'planned_date_end': "2021-04-07 15:00:00",
            'project_id': cls.project_test.id})
