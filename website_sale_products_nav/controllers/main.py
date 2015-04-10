# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

import openerp.addons.website_sale.controllers.main
from openerp import http
from openerp.http import request


class WebsiteSale(openerp.addons.website_sale.controllers.main.website_sale):
    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/'
        '<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', **post):
        r = super(WebsiteSale, self).shop(page=page, category=category,
                                          search=search, **post)

        cr, uid, context, pool, website = (request.cr, request.uid,
                                           request.context, request.registry,
                                           request.website)

        domain = website.sale_product_domain()
        if search:
            domain += ['|', '|', '|', ('name', 'ilike', search),
                       ('description', 'ilike', search),
                       ('description_sale', 'ilike', search),
                       ('product_variant_ids.default_code', 'ilike', search)]
        if category:
            domain += [('product_variant_ids.public_categ_ids', 'child_of',
                        int(category))]

        product_obj = pool.get('product.template')
        # Order defecto Odoo
        # 'website_published desc, website_sequence desc'
        order = 'asc'
        if 'order' in request.httprequest.args.getlist.im_self:
            # Comprobamos que el parámetro order de la url es 'asc|desc'
            order = 'desc' if \
                request.httprequest.args.getlist.im_self['order'] == 'desc' \
                else order

        order_by = ''
        search_order = 'website_sequence {1}{2}'.format(
            order_by,
            order,
            ', name asc'
        )
        if 'orderby' in request.httprequest.args.getlist.im_self:
            if request.httprequest.args.getlist.im_self['orderby'] == 'price':
                order_by = 'price'
                search_order = 'list_price {1}{2}'.format(
                    order_by,
                    order,
                    ', website_sequence asc, name asc'
                )
            elif request.httprequest.args.getlist.im_self['orderby'] == 'name':
                order_by = 'name'
                search_order = 'name {1}{2}'.format(
                    order_by,
                    order,
                    ', website_sequence asc'
                )
        product_ids = product_obj.search(
            cr, uid, domain, limit=website.shop_products_per_page,
            # bug reportado https://github.com/odoo/odoo/issues/3373
            # bug aceptado https://github.com/odoo/odoo/commit/
            #   93e4e7da6e70f2283d7fa92ff1eda6ec41772de0
            # cr, uid, domain, limit=PPG+10,
            offset=r.qcontext['pager']['offset'],
            order=search_order,
            context=context)
        products = product_obj.browse(cr, uid, product_ids, context=context)

        r.qcontext['products'] = products
        r.qcontext['products_nav'] = {
            'order': order,
            'orderby': order_by,
            'default_url': '{0}?order={1}'.format(
                request.httprequest.base_url, 'desc' if order == 'asc'
                and order_by == '' else 'asc'),
            'price_url': '{0}?orderby=price&order={1}'.format(
                request.httprequest.base_url, 'desc' if order == 'asc'
                and order_by == 'price' else 'asc'),
            'name_url': '{0}?orderby=name&order={1}'.format(
                request.httprequest.base_url, 'desc' if order == 'asc'
                and order_by == 'name' else 'asc')
        }

        return r
