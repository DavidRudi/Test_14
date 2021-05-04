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

    def test_create_purchase_from_workflow(self):

        document_gif = self.env['documents.document'].create({
            'datas': GIF,
            'name': 'file.gif',
            'mimetype': 'image/gif',
            'folder_id': self.folder_po.id,
        })

        workflow_rule = self.env['documents.workflow.rule'].create({
            'domain_folder_id': self.folder_po.id,
            'name': 'workflow purchase',
            'create_model': 'purchase.order',
        })

        action = workflow_rule.apply_actions([document_gif.id])
        new_purchase_order = self.env['purchase.order'].browse([action['res_id']])

        self.assertEqual(document_gif.res_model, 'purchase.order')
        self.assertEqual(document_gif.res_id, new_purchase_order.id)

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
            'partner_id': self.env.user.partner_id.id,
            'company_id': company_test.id
        })
        purchase_test_a = self.env['purchase.order'].create({
            'name': 'po_test_a',
            'partner_id': self.env.user.partner_id.id,
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

