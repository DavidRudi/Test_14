# -*- coding: utf-8 -*-

import base64
from odoo.tests.common import HttpCase, tagged, SavepointCase, TransactionCase

GIF = b"R0lGODdhAQABAIAAAP///////ywAAAAAAQABAAACAkQBADs="
TEXT = base64.b64encode(bytes("workflow bridge sale order", 'utf-8'))


@tagged('cluedoo')
class TestCaseDocumentsBridgeSale(TransactionCase):

    def setUp(self):
        super(TestCaseDocumentsBridgeSale, self).setUp()
        self.folder_so = self.env['documents.folder'].create({
            'name': 'folder SO',
        })
        self.folder_so_a = self.env['documents.folder'].create({
            'name': 'folder A - A',
            'parent_folder_id': self.folder_so.id,
        })
        self.attachment_txt = self.env['documents.document'].create({
            'datas': TEXT,
            'name': 'file.txt',
            'mimetype': 'text/plain',
            'folder_id': self.folder_so_a.id,
        })
        self.workflow_rule_task = self.env['documents.workflow.rule'].create({
            'domain_folder_id': self.folder_so.id,
            'name': 'workflow rule create task on f_a',
            'create_model': 'sale.order',
        })

    def test_bridge_folder_workflow(self):
        """
        tests the create new business model (sale).

        """
        self.assertEqual(self.attachment_txt.res_model, 'documents.document', "failed at default res model")
        self.workflow_rule_task.apply_actions([self.attachment_txt.id])

        self.assertEqual(self.attachment_txt.res_model, 'sale.order', "failed at workflow_bridge_documents_sale_order"
                                                                        " new res_model")
        so = self.env['sale.order'].search([('id', '=', self.attachment_txt.res_id)])
        self.assertTrue(so.exists(), 'failed at workflow_bridge_documents_sale_order so')
        self.assertEqual(self.attachment_txt.res_id, so.id, "failed at workflow_bridge_documents_sale_order res_id")

    def test_bridge_sale_project_settings_on_write(self):
        """
        Makes sure the settings apply their values when an document is assigned a res_model, res_id
        """
        folder_test = self.env['documents.folder'].create({'name': 'folder_test'})

        company_test = self.env['res.company'].create({
            'name': 'test bridge sales',
            'sale_folder': folder_test.id,
            'documents_project_settings': False
        })
        order_test = self.env['sale.order'].create({
            'name': 'sale_order_test',
            'company_id': company_test.id
        })
        attachment_txt_test = self.env['ir.attachment'].create({
            'datas': TEXT,
            'name': 'fileText_test.txt',
            'mimetype': 'text/plain',
        })

        company_test.write({'documents_project_settings': True})

        attachment_txt_test.write({
            'res_model': 'sale.order',
            'res_id': order_test.id
        })

        txt_doc = self.env['documents.document'].search([('attachment_id', '=', attachment_txt_test.id)])

        self.assertEqual(txt_doc.folder_id, folder_test, 'the text test document have a folder')
