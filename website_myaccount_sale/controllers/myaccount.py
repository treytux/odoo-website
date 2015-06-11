# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp import http
from openerp.http import request


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

    @http.route(['/myaccount/orders'],
                type='http', auth='public', website=True)
    def orders(self, container=None, **post):
        env = request.env
        partner = self.get_partner_company()
        if partner:
            orders = env['sale.order'].sudo().search(
                [('partner_id', '=', partner.id),
                 ('state', 'not in', ['cancel'])])
        else:
            orders = []
        return request.website.render(
            'website_myaccount_sale.orders',
            {'orders': orders})


    @http.route(['/myaccount/order/download/<int:order_id>'],
                type='http', auth='public', website=True)
    def order_download(self, order_id, **post):
        env = request.env
        order = env['sale.order'].browse(order_id)
        if order.exists() and order.sudo().partner_id.id == \
                env.user.partner_id.id:
            pdf = env['report'].sudo().get_pdf(order,
                                               'sale.report_saleorder')
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return '' # The Silence is Golden
