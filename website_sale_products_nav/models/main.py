# -*- coding: utf-8 -*-
###############################################################################
#
#    Trey, Kilobytes de Soluciones
#    Copyright (C) 2014-Today Trey, Kilobytes de Soluciones <www.trey.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import openerp.addons.website_sale.controllers.main
from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import PPG


class WebsiteSale(openerp.addons.website_sale.controllers.main.website_sale):
    @http.route(['/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', **post):
        r = super(WebsiteSale, self).shop(page=page, category=category,
                                          search=search, **post)

        cr, uid, context, pool = (request.cr, request.uid, request.context,
                                  request.registry)

        domain = request.website.sale_product_domain()
        if search:
            domain += ['|', '|', '|', ('name', 'ilike', search),
                       ('description', 'ilike', search),
                       ('description_sale', 'ilike', search),
                       ('product_variant_ids.default_code', 'ilike', search)]
        if category:
            domain += [('product_variant_ids.public_categ_ids', 'child_of',
                        int(category))]

        product_obj = pool.get('product.template')
        product_ids = product_obj.search(
            cr, uid, domain, limit=PPG+10,
            offset=r.qcontext['pager']['offset'],
            order='list_price asc, website_published desc, website_sequence desc',
            context=context)
        products = product_obj.browse(cr, uid, product_ids, context=context)

        r.qcontext['products'] = products

        return r
