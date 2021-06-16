import io
import base64
import logging
from odoo import models, api, fields
from odoo.tools.safe_eval import safe_eval
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

_logger = logging.getLogger(__name__)

class SnailmailLetter(models.Model):
    _inherit = 'snailmail.letter'
    _description = 'Snailmail Letter'

    snailmail_records = fields.One2many('snailmail.lines', 'snail_mail_id', string='Snail Mail Records')
    attachment_datas = fields.Binary('Document', compute='compute_attachment', store=True, related=False)
    is_snailmail_merge = fields.Boolean(string='is snailmail merge')

    @api.onchange("snailmail_records")
    def onchange_snailmail_line(self):
        if (len(self.snailmail_records.model_id) != 0):
            self.model = self.snailmail_records[0].model_id.model
            self.res_id = self.snailmail_records[0].document_id

    @api.depends('attachment_id','is_snailmail_merge','snailmail_records')
    def compute_attachment(self):
        for merge in self:
            if merge.is_snailmail_merge:
                merger = PdfFileMerger()
                output = io.BytesIO()
                for snailmail_line in merge.snailmail_records:
                    if snailmail_line.document:
                        merger.append(PdfFileReader(io.BytesIO(base64.b64decode(snailmail_line.document)), strict=False, overwriteWarnings=False), import_bookmarks=False)
                merger.write(output)
                merger.close()
                merge.attachment_datas = base64.b64encode(output.getvalue())
            else:
                if merge.attachment_id:
                    merge.attachment_datas = merge.attachment_id.datas
                else:
                    merge.attachment_datas = False

    def mergerPdfs(self):
        for snailmail in self:
            return snailmail

    def _snailmail_print(self, immediate=True):
        res = super(SnailmailLetter, self)._snailmail_print(immediate)
        ctx = dict(self._context)
        is_merge = ctx.get('is_merge')
        if len(self) != 1 and is_merge:
            snailmail_line = []
            for letter in self:
                letter._fetch_attachment()
                model_id = self.env['ir.model'].search([('model','=',letter.model)])
                values = (0,0,{
                    'document_id': letter.res_id,
                    'model_id': model_id.id,
                    'document': letter.attachment_datas
                })
                snailmail_line.append(values)

            main_snailmail = self.env['snailmail.letter'].create({
                'partner_id': letter.partner_id.id,
                'model': 'account.move',
                'res_id': letter.res_id,
                'user_id': self.env.user.id,
                'company_id': letter.company_id.id,
                'report_template': self.env.ref('account.account_invoices').id,
                'is_snailmail_merge': True,
                'snailmail_records': snailmail_line
            })
            for letter in self:
                letter.unlink()
        return res

class SnailMailLine(models.Model):
    _name = "snailmail.lines"
    _description = "Snail Mail Lines"

    snail_mail_id = fields.Many2one('snailmail.letter', string='Related Record')
    model_id = fields.Many2one('ir.model', string='Models', ondelete='cascade')
    document_id = fields.Integer(string='Document ID', required=True)
    document = fields.Binary(string='Document')
    file_name = fields.Char(string='File Name', size=256)
    references_id = fields.Char(string ='References', compute='_compute_reference', readonly=True, store=False)

    @api.depends('model_id', 'document_id')
    def _compute_reference(self):
        for res in self:
            res.references_id = "%s,%s" % (res.model_id.model, res.document_id)
 