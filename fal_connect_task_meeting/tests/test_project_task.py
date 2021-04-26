from odoo.tests.common import TransactionCase
from odoo.addons.project.tests.test_project_base import TestProjectCommon
from odoo.tests import Form, tagged
from odoo.exceptions import UserError


@tagged('cluedoo')
class TestProjectTask(TestProjectCommon):
    @classmethod
    def setUpClass(cls):
        super(TestProjectTask, cls).setUpClass()

        user_group_employee = cls.env.ref('base.group_user')
        user_group_project_manager = cls.env.ref('project.group_project_manager')

        Users = cls.env['res.users'].with_context({'no_reset_password': True})
        cls.user_projecttask = Users.create({
            'name': 'Didier Drogba',
            'login': 'D',
            'email': 'drogba@example.com',
            'groups_id': [(6, 0, [user_group_employee.id, user_group_project_manager.id])]})

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
            'project_id': cls.user_projecttask.id})
