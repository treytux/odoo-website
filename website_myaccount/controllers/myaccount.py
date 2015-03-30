# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.
from openerp import http
from openerp.http import request


class MyAccount(http.Controller):

    @http.route([
        '/myaccount',
        ], type='http', auth="public", website=True)
    def myaccount(self, container=None, **post):
        return request.website.render('website_myaccount.dashboard', {})
