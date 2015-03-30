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

from openerp import models, fields, api, _
from openerp.exceptions import Warning
from openerp.addons.website_sale.controllers import main

import logging
_log = logging.getLogger(__name__)


class website(models.Model):
    _inherit = 'website'

    shop_products_per_page = fields.Integer(u'Products per page', default=20)

    @api.one
    @api.constrains('shop_products_per_page')
    def _check_seats_limit(self):
        if self.shop_products_per_page <= 0:
            raise Warning(_('Products per page must be greater than zero.'))

    def read(self, cr, user, ids, fields=None, context=None,
             load='_classic_read'):
        r = super(website, self).read(cr, user, ids, fields, context, load)
        if 'shop_products_per_page' in r[0]:
            main.__dict__['PPG'] = r[0]['shop_products_per_page']
        return r
