from odoo import _, api, fields, models, tools
import logging

_logger = logging.getLogger(__name__)


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'
    _name = "mail.compose.message"

    def get_followers(self):
        active_id = self._context.get('active_id')
        model = self._context.get('active_model')
        find_followers_mail_ids = self.env['mail.followers'].search([('res_model', '=', model), ('res_id', '=', active_id)])

        values = []
        for follower in find_followers_mail_ids:
            partner = follower.partner_id
            values.append(partner.id)
        return [(6, 0, values)]

    fal_select_tags_followers = fields.Many2many(
        'res.partner', 'fal_mail_compose_message_res_partner_rel',
        'wizard_id', 'partner_id', 'Followers',
        domain=[('type', '!=', 'private')], default=get_followers)

    def send_mail(self, auto_commit=False):
        self.partner_ids = self.fal_select_tags_followers

        res = super(MailComposeMessage, self).send_mail(auto_commit=auto_commit)
        return res
        

        
