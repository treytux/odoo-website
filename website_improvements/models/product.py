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

from openerp import models, fields
# from openerp import tools, SUPERUSER_ID
# from openerp.osv import fields, orm
# from openerp.tools.translate import _


class product_template(models.Model):
    _inherit = "product.template"

    public_name = fields.Char(u'Public Name', required=False, translate=True,
                              select=True,
                              help=u'Public name for products in eCommerce')

    def create(self, cr, uid, vals, context=None):
        if 'public_name' not in vals:
            vals['public_name'] = vals['name']
        return super(product_template, self).create(cr, uid, vals, context)
