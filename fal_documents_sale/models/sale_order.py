# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'documents.mixin']

    def _get_document_tags(self):
        return self.company_id.sale_tags

    def _get_document_folder(self):
        return self.company_id.sale_folder

    def _check_create_documents(self):
        return self.company_id.documents_sale_settings and super()._check_create_documents()
