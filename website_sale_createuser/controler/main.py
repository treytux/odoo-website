# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp.addons.web.controllers.main import login_redirect
import openerp.addons.website_sale.controllers.main as main


class WebsiteSale(main.website_sale):

    def get_partner_company(self):
        user = request.env.user
        if user.partner_id.is_company:
            return user.partner_id
        else:
            partner = user.partner_id
            while partner.parent_id:
                partner = partner.parent_id
                if partner.is_company:
                    return partner
        return None

    @http.route(['/shop/confirmation'], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        cr, uid, context = request.cr, request.uid, request.context

        res = super(WebsiteSale, self).payment_confirmation()
        if res.qcontext['order']:
            order = res.qcontext['order']
            env = request.env

            if request.uid != request.website.user_id.id:
                partner = self.get_partner_company()
                if partner and partner.id == order.partner_id.id:
                    return request.website.render(
                        "website_sale.confirmation", {'order': order})
            else:
                value = {
                    'name': order.partner_id.name,
                    'login': order.partner_id.email,
                    'partner_id': order.partner_id.id,
                    'in_group_2': True,
                    'in_group_11': False,
                    'sel_groups_24_25_26': 0,
                    'sel_groups_5': 0,
                    'sel_groups_22_23': 0,
                    'sel_groups_21': 0,
                    'sel_groups_3_4': 0,
                    'share': True,
                }
                user = request.env['res.users'].sudo().create(value)
                return request.website.render(
                    "website_sale.confirmation", {'order': order})
