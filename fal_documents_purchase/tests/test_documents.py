# -*- coding: utf-8 -*-

import base64
from odoo.tests.common import HttpCase, tagged, SavepointCase, TransactionCase

GIF = b"R0lGODdhAQABAIAAAP///////ywAAAAAAQABAAACAkQBADs="
TEXT = base64.b64encode(bytes("workflow bridge sale order", 'utf-8'))


@tagged('cluedoo')
class TestCaseDocumentsBridgePurchase(TransactionCase):

    def setUp(self):
        super(TestCaseDocumentsBridgePurchase, self).setUp()
        self.folder_po = self.env['documents.folder'].create({
            'name': 'folder PO',
        })
        self.folder_po_a = self.env['documents.folder'].create({
            'name': 'folder P - O',
            'parent_folder_id': self.folder_po.id,
        })
        self.attachment_txt = self.env['documents.document'].create({
            'datas': TEXT,
            'name': 'file.txt',
            'mimetype': 'text/plain',
            'folder_id': self.folder_po_a.id,
        })
        self.workflow_rule_task = self.env['documents.workflow.rule'].create({
            'domain_folder_id': self.folder_po.id,
            'name': 'workflow rule create task on f_a',
            'create_model': 'purchase.order',
        })

    def test_bridge_folder_workflow(self):
        """
        tests the create new business model (project).

        """
        self.assertEqual(self.attachment_txt.res_model, 'documents.document', "failed at default res model")
        self.workflow_rule_task.apply_actions([self.attachment_txt.id])

        self.assertEqual(self.attachment_txt.res_model, 'purchase.order', "failed at workflow_bridge_documents_purchase"
                                                                        " new res_model")
        po = self.env['purchase.order'].search([('id', '=', self.attachment_txt.res_id)])
        self.assertTrue(so.exists(), 'failed at workflow_bridge_documents_purchase order')
        self.assertEqual(self.attachment_txt.res_id, po.id, "failed at workflow_bridge_documents_purchase res_id")

    def test_bridge_purchase_settings_on_write(self):
        """
        Makes sure the settings apply their values when an document is assigned a res_model, res_id
        """
        folder_test = self.env['documents.folder'].create({'name': 'folder_test_purchase'})

        company_test = self.env['res.company'].create({
            'name': 'test bridge purchase',
            'purchase_folder': folder_test.id,
            'documents_purchase_settings': False
        })
        purchase_test = self.env['purchase.order'].create({
            'name': 'po_test',
            'company_id': company_test.id
        })
        purchase_test_a = self.env['purchase.order'].create({
            'name': 'po_test_a',
            'company_id': company_test.id
        })
        attachment_txt_test = self.env['ir.attachment'].create({
            'datas': TEXT,
            'name': 'fileText_test.txt',
            'mimetype': 'text/plain',
        })
        attachment_gif_test = self.env['ir.attachment'].create({
            'datas': GIF,
            'name': 'fileText_test.txt',
            'mimetype': 'text/plain',
        })

        company_test.write({'documents_purchase_settings': True})

        attachment_txt_test.write({
            'res_model': 'purchase.order',
            'res_id': purchase_test.id
        })
        attachment_gif_test.write({
            'res_model': 'purchase.order',
            'res_id': purchase_test_a.id
        })

        txt_doc = self.env['documents.document'].search([('attachment_id', '=', attachment_txt_test.id)])
        gif_doc = self.env['documents.document'].search([('attachment_id', '=', attachment_gif_test.id)])

        self.assertEqual(txt_doc.folder_id, folder_test, 'the text test document have a folder')
        self.assertEqual(gif_doc.folder_id, folder_test, 'the gif test document have a folder')

