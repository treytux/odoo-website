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


class ContactUs(openerp.addons.website_crm.controllers.main.contactus):
    @http.route(['/crm/contactus'], type='http', auth="public", website=True)
    def contactus(self, **kwargs):
        pass
        # r = super(ContactUs, self).contactus(**kwargs)
        # return self.get_contactus_response(values, kwargs)
