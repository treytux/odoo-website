# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp import http
from openerp.http import request


class MyAccount(http.Controller):

    @http.route(['/myaccount'], type='http', auth='public', website=True)
    def myaccount(self, container=None, **post):
        return request.website.render('website_myaccount.dashboard', {})

    @http.route(['/myaccount/profile'],
                type='http', auth='public', website=True)
    def profile(self, container=None, **post):
        return request.website.render('website_myaccount.profile', {
            'user': request.env.user
            })

    @http.route(['/myaccount/profile/update'], type='json', auth='public',
                methods=['POST'], website=True)
    def profile_update(self, data):
        env = request.env

        if 'email' in data and env.user.email != data['email']:
            exist = env.user.search([('email', '=', data['email'])])
            if exist:
                return {'error': 'The email %s have ', 'result': False}

        result = env.user.write(data)
        return {'error': '', 'result': result}

    @http.route(['/myaccount/addresses'],
                type='http', auth='public', website=True)
    def addresses(self, container=None, **post):
        env = request.env
        partner = self.get_partner_company() or env.user.partner_id
        shipping = [p for p in partner.child_ids if p.type == 'delivery']
        invoices = [p for p in partner.child_ids if p.type == 'invoice']
        return request.website.render('website_myaccount.addresses', {
            'shipping_address': shipping,
            'invoice_address': invoices})
