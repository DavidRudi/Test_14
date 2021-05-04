# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order', 'documents.mixin']

    def _get_document_tags(self):
        return self.company_id.purchase_tags

    def _get_document_folder(self):
        return self.company_id.purchase_folder

    def _check_create_documents(self):
        return self.company_id.documents_purchase_settings and super()._check_create_documents()
