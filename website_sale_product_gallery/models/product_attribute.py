# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################

from openerp import fields, api
from openerp.osv import osv


class ProductAttribute(osv.osv):
    _inherit = "product.attribute"

    affects_image = fields.Boolean(string=u"Afecta a la imagen del producto")


class ProductAttributeValue(osv.osv):
    _inherit = "product.attribute.value"

    affects_image = fields.Boolean(compute='_compute_affects_image',
                                   store=True)

    @api.one
    @api.depends('attribute_id', 'attribute_id.affects_image')
    def _compute_affects_image(self):
        self.affects_image = self.attribute_id.affects_image
