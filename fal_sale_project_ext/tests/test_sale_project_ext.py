from odoo.tests.common import SavepointCase, tagged


@tagged('cluedoo')
class TestSaleProjectExt(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create project template
        cls.analytic_account_sale = cls.env['account.analytic.account'].create({
            'name': 'Project for selling timesheet - SPX',
            'code': 'SPX-2222'
        })
        cls.project_template_ext = cls.env['project.project'].create({
            'name': 'Project Template New',
            'privacy_visibility': 'portal',
            'fal_is_template': True,
            'delay_count': 3,
        })
        cls.project_template_state = cls.env['project.task.type'].create({
            'name': 'Only stage in project template',
            'sequence': 1,
            'project_ids': [(4, cls.project_template_ext.id)]
        })
        # Create service products
        uom_hour = cls.env.ref('uom.product_uom_hour')

        cls.product_order_service3 = cls.env['product.product'].create({
            'name': "Service Ordered, create task in new project based on template",
            'standard_price': 10,
            'list_price': 20,
            'type': 'service',
            'invoice_policy': 'order',
            'uom_id': uom_hour.id,
            'uom_po_id': uom_hour.id,
            'default_code': 'SERV-ORDERED3',
            'service_tracking': 'task_in_project',
        })

        cls.product_order_service4 = cls.env['product.product'].create({
            'name': "Service Ordered, create project only",
            'standard_price': 15,
            'list_price': 30,
            'type': 'service',
            'invoice_policy': 'order',
            'uom_id': uom_hour.id,
            'uom_po_id': uom_hour.id,
            'default_code': 'SERV-ORDERED4',
            'service_tracking': 'project_only',
            'project_id': False,
        })

    def test_sale_order_with_project_task(self):
        SaleOrderLine = self.env['sale.order.line'].with_context(tracking_disable=True)

        partner = self.env['res.partner'].create({'name': "Test Sale1"})
        sale_order = self.env['sale.order'].with_context(tracking_disable=True).create({
            'partner_id': partner.id,
            'partner_invoice_id': partner.id,
            'partner_shipping_id': partner.id,
            'project_template_id': self.project_template_ext.id,
        })

        so_line_order_new_task_new_project = SaleOrderLine.create({
            'name': self.product_order_service3.name,
            'product_id': self.product_order_service3.id,
            'product_uom_qty': 10,
            'product_uom': self.product_order_service3.uom_id.id,
            'price_unit': self.product_order_service3.list_price,
            'order_id': sale_order.id,
        })

        so_line_order_only_project = SaleOrderLine.create({
            'name': self.product_order_service4.name,
            'product_id': self.product_order_service4.id,
            'product_uom_qty': 10,
            'product_uom': self.product_order_service4.uom_id.id,
            'price_unit': self.product_order_service4.list_price,
            'order_id': sale_order.id,
        })
        sale_order.action_confirm()

        #  service_tracking 'task_in_project'
        self.assertTrue(so_line_order_new_task_new_project.project_id, "Sales order line should be linked to newly created project")
        self.assertTrue(so_line_order_new_task_new_project.task_id, "Sales order line should be linked to newly created task")
        # service_tracking 'project_only'
        self.assertFalse(so_line_order_only_project.task_id, "Task should not be created")
        self.assertTrue(so_line_order_only_project.project_id, "Sales order line should be linked to newly created project")
