# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.addons.report.controllers.main import ReportController



class MyAccount(http.Controller):

    def get_partner_company(self):
        user = request.env.user
        if user.partner_id.is_company:
            return user.partner_id
        else:
            partner = user.partner_id
            if partner.parent_id:
                while partner.parent_id:
                    partner = partner.parent_id
                    if partner.is_company:
                        return partner
            else:
                return partner
        return None

    @http.route(['/myaccount/invoices'],
                type='http', auth='public', website=True)
    def invoices(self, **post):
        env = request.env
        partner = self.get_partner_company()
        if partner:
            invoices = env['account.invoice'].sudo().search(
                [('partner_id', '=', partner.id),
                 ('state', 'not in', ['draft', 'cancel'])])
        else:
            invoices = []
        return request.website.render(
            'website_myaccount_invoice.invoices',
            {'invoices': invoices})

    @http.route(['/myaccount/invoice/download/<int:invoice_id>'],
                type='http', auth='public', website=True)
    def invoice_download(self, invoice_id, **post):
        env = request.env
        invoice = env['account.invoice'].browse(invoice_id)
        if invoice.exists() and invoice.sudo().partner_id.id == \
                env.user.partner_id.id:
            pdf = env['report'].sudo().get_pdf(invoice, 'account.report_invoice')
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return '' # The Silence is Golden
