# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp.addons.website_sale.controllers import main


class website_config_settings(osv.osv_memory):
    _inherit = 'website.config.settings'

    _columns = {
        'shop_products_per_page': fields.related(
            'website_id',
            'shop_products_per_page',
            type="integer",
            string='Products per page'),
    }

    _defaults = {
        'shop_products_per_page': 20,
    }

    def read(self, cr, user, ids, fields=None, context=None,
             load='_classic_read'):
        r = super(website_config_settings, self).read(
            cr, user, ids, fields, context, load)

        if 'shop_products_per_page' in r[0]:
            main.__dict__['PPG'] = r[0]['shop_products_per_page']

        return r
