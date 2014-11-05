# -*- coding: utf-8 -*-
##############################################################################
#
#    Trey, Kilobytes de Soluciones
#    Copyright (C) 2014-Today Trey, Kilobytes de Soluciones
#    (<http://www.trey.es>).
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
##############################################################################
import openerp.addons.website_sale.controllers.main as main

from openerp import SUPERUSER_ID
from openerp.http import request

import logging
_log = logging.getLogger(__name__)


class WebsiteSale(main.website_sale):

    def checkout_values(self, data=None):
        result = super(WebsiteSale, self).checkout_values(data=data)

        result['checkout']['comments_order'] = \
            data.get('comments_order', None) if data else None

        return result

    def checkout_form_save(self, checkout):
        result = super(WebsiteSale, self).checkout_form_save(checkout)

        if 'comments_order' in checkout and checkout['comments_order']:
            cr, context = request.cr, request.context
            order_obj = request.registry.get('sale.order')

            order = request.website.sale_get_order(force_create=1,
                                                   context=context)

            order_obj.write(cr, SUPERUSER_ID, [order.id], {
                'note': checkout['comments_order']
            }, context=context)

        return result
