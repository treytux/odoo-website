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

import logging
_log = logging.getLogger(__name__)


class GalleryImageProductPublicCategory(models.Model):
    _inherit = "gallery_image"
    _name = "product_public_category.gallery_image"
    _description = "Gallery Image for product.public.category"

    category_id = fields.Many2one('product.public.category',
                                  u'Public Category')

    @property
    def object_relation_name(self):
        return "category_id"


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    gallery_ids = fields.One2many('product_public_category.gallery_image',
                                  'category_id')

    def write(self, cr, uid, ids, vals, context=None):
        r = super(ProductPublicCategory, self).write(cr, uid, ids, vals,
                                                     context)
        self.pool['gallery_image'].update_sequences_gallery(
            cr, uid, ids, self, 'gallery_ids',
            'product_public_category.gallery_image')
        return r
