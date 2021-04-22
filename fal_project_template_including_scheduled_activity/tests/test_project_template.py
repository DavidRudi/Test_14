from odoo.tests.common import TransactionCase
from odoo.addons.project.tests.test_project_base import TestProjectCommon
from odoo.tests import Form, tagged
from odoo.exceptions import UserError


@tagged('cluedoo')
class TestProjectTemplate(TestProjectCommon):
    @classmethod
    def setUpClass(cls):
        super(TestProjectTemplate, cls).setUpClass()

        user_group_employee = cls.env.ref('base.group_user')
        user_group_project_user = cls.env.ref('project.group_project_user')
        user_group_project_manager = cls.env.ref('project.group_project_manager')

        cls.partner_1a = cls.env['res.partner'].create({
            'name': 'Valid L',
            'email': 'valid.l@agrolait.com'})
        cls.partner_2a = cls.env['res.partner'].create({
            'name': 'Valid O',
            'email': 'valid.O@gmail.com'})
        cls.partner_3a = cls.env['res.partner'].create({
            'name': 'Valid P',
            'email': 'valid.p@gmail.com'})

        # Test users to use through the various tests
        Users = cls.env['res.users'].with_context({'no_reset_password': True})
        cls.user_public = Users.create({
            'name': 'P',
            'login': 'P',
            'email': 'P@example.com',
            'signature': 'P',
            'notification_type': 'email',
            'groups_id': [(6, 0, [cls.env.ref('base.group_public').id])]})
        cls.user_portal = Users.create({
            'name': 'Z',
            'login': 'Z',
            'email': 'Z@gladys.portal',
            'signature': 'Z',
            'notification_type': 'email',
            'groups_id': [(6, 0, [cls.env.ref('base.group_portal').id])]})
        cls.user_projectuser = Users.create({
            'name': 'A ProjectUser',
            'login': 'A',
            'email': 'Aprojectuser@example.com',
            'groups_id': [(6, 0, [user_group_employee.id, user_group_project_user.id])]
        })
        cls.user_projectmanager = Users.create({
            'name': 'B ProjectManager',
            'login': 'B',
            'email': 'B.projectmanager@example.com',
            'groups_id': [(6, 0, [user_group_employee.id, user_group_project_manager.id])]})

        # Test 'Template' project
        cls.project_template = cls.env['project.project'].with_context({'mail_create_nolog': True}).create({
            'name': 'Project Template',
            'privacy_visibility': 'portal',
            'fal_is_template': True,
            'delay_count': 3,
            'partner_id': cls.partner_1.id})
        # Already-existing tasks in Pigs
        cls.task_1 = cls.env['project.task'].with_context({'mail_create_nolog': True}).create({
            'name': 'Template UserTask',
            'delay_count': 4,
            'assignment_logic': "result = user.search([('name', '=', 'A ProjectUser')])",
            'project_id': cls.project_template.id})

    def test_create_project_from_template(self):
        """Create project from project template"""
        project_new = self.project_template.take_template()

        self.assertTrue(project_new.ref)
