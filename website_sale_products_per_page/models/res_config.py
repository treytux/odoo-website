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

from openerp.osv import fields, osv


class website_config_settings(osv.osv_memory):
    _inherit = 'website.config.settings'

    _columns = {
        'website_id': fields.many2one('website', string="website",
                                      required=True),
        'shop_products_per_page': fields.related(
            'website_id',
            'shop_products_per_page',
            type="integer",
            string='Products per page'),
    }

    _defaults = {
        'shop_products_per_page': 20,
        'website_id': lambda self, cr, uid, c:
        self.pool.get('website').search(cr, uid, [], context=c)[0],
    }

    def on_change_website_id(self, cr, uid, ids, website_id, context=None):
        website_data = self.pool.get('website').read(cr, uid, [website_id], [],
                                                     context=context)[0]
        values = {}
        for fname, v in website_data.items():
            if fname in self._columns:
                values[fname] = v[0] if v \
                    and self._columns[fname]._type == 'many2one' else v

        return {'value': values}

    # FIXME in trunk for god sake. Change the fields above to fields.char
    # instead of fields.related, and create the function set_website who
    # will set the value on the website_id create does not forward the
    # values to the related many2one. Write does.
    def create(self, cr, uid, vals, context=None):
        config_id = super(website_config_settings, self).create(
            cr, uid, vals, context=context)
        self.write(cr, uid, config_id, vals, context=context)
        return config_id
