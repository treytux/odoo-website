# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug


class website_sale_wishlist_products(http.Controller):

    @http.route(['/wishlist'], type='http', auth="public", methods=['GET'], website=True)
    def wishlist_list(self):
        """
        Obtiene la lista de deseos para un usuario en el sitio web indicado
        """
        cr, uid, context, registry, website = request.cr, request.uid, request.context, request.registry, request.website

        values = {}
        orm_wishlist = registry.get('wishlist')
        wishlist_ids = orm_wishlist.search(cr, SUPERUSER_ID, [
            ('website_id', '=', website.id),
            ('user_id', '=', uid)], context=context, limit=1)
        if wishlist_ids:
            orm_wishlist_products = registry.get('wishlist_products')
            wishlist_products_ids = orm_wishlist_products.search(cr, SUPERUSER_ID, [
                ('wishlist_id', '=', wishlist_ids[0])], context=context, limit=1)
            if wishlist_products_ids:
                wishlist_products = orm_wishlist_products.browse(cr, SUPERUSER_ID, wishlist_products_ids, context)
                values = {
                    'wishlist_id': wishlist_ids[0],
                    'wishlist_products': wishlist_products,
                }

        return request.website.render("website_sale_wishlist_products.wishlist_list", values)

    @http.route(['/wishlist/add'], type='json', auth="public", methods=['POST'], website=True)
    def wishlist_set(self, product_tmpl_id):
        """
        Añade un producto a la lista de deseos del usuario en el sitio web indicado
        """
        cr, uid, context, registry, website = request.cr, request.uid, request.context, request.registry, request.website

        orm_wishlist = registry.get('wishlist')
        wishlist_ids = orm_wishlist.search(cr, SUPERUSER_ID, [
            ('website_id', '=', website.id),
            ('user_id', '=', uid)], context=context, limit=1)
        if not wishlist_ids:
            wishlist_ids = orm_wishlist.create(cr, SUPERUSER_ID, {
                'website_id': website.id,
                'user_id': uid,
            })
        orm_wishlist_products = registry.get('wishlist_products')
        wishlist_products_ids = orm_wishlist_products.search(cr, SUPERUSER_ID, [
            ('wishlist_id', '=', wishlist_ids[0]),
            ('product_tmpl_id', '=', product_tmpl_id)], context=context, limit=1)
        if not wishlist_products_ids:
            wishlist_products_ids = orm_wishlist_products.create(cr, SUPERUSER_ID, {
                'wishlist_id': wishlist_ids[0],
                'product_tmpl_id': product_tmpl_id,
            })

        return {
            'user_id': uid,
            'website_id': website.id,
            'product_tmpl_id': product_tmpl_id
        }

    @http.route(['/wishlist/remove'], type='json', auth="public", methods=['POST'], website=True)
    def wishlist_remove(self, wishlist_product_id):
        """
        Elimina un producto de la lista de deseos del usuario en el sitio web indicado
        """
        cr, uid, context, registry, website = request.cr, request.uid, request.context, request.registry, request.website

        orm_wishlist_products = registry.get('wishlist_products')
        orm_wishlist_products.unlink(cr, uid, int(wishlist_product_id))

        return {
            'wishlist_product_id': wishlist_product_id,
        }

    @http.route(['/wishlist/empty'], type='json', auth="public", methods=['POST'], website=True)
    def wishlist_empty(self, wishlist_id):
        """
        Vacia la lista de deseos del usuario en el sitio web indicado
        """
        cr, uid, context, registry, website = request.cr, request.uid, request.context, request.registry, request.website

        orm_wishlist_products = registry.get('wishlist_products')
        wishlist_products_ids = orm_wishlist_products.search(cr, SUPERUSER_ID, [
            ('wishlist_id', '=', wishlist_id)], context=context)
        if wishlist_products_ids:
            orm_wishlist_products.unlink(cr, uid, wishlist_products_ids)

        return {
            'wishlist_id': wishlist_id,
        }
