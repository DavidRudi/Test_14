from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    project_template_id = fields.Many2one(domain="[('fal_is_template', '=', True)]")
