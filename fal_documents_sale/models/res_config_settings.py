# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    documents_sale_settings = fields.Boolean(related='company_id.documents_sale_settings', readonly=False,
                                                string="Sale")
    sale_folder = fields.Many2one('documents.folder', related='company_id.sale_folder', readonly=False,
                                     string="Sale default workspace")
    sale_tags = fields.Many2many('documents.tag', 'sale_tags_table',
                                    related='company_id.sale_tags', readonly=False,
                                    string="Sale Tags")

    @api.onchange('sale_folder')
    def on_sale_folder_change(self):
        if self.sale_folder != self.sale_tags.mapped('folder_id'):
            self.sale_tags = False
