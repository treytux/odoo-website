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
from .gallery_image import update_sequences_gallery

import logging
_log = logging.getLogger(__name__)


class GalleryImageTemplate(models.Model):
    _inherit = "gallery_image"
    _name = "product_template.gallery_image"
    _description = "Gallery Image for product.template"

    product_tmpl_id = fields.Many2one('product.template', u'Product Template')
    attribute_value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        relation='product_template_gallery_image_product_attribute_value_rel',
        column1='image_id',
        column2='att_id'
    )

    @property
    def object_relation_name(self):
        return "product_tmpl_id"

    def compute_name_image(self, name=None, sequence=None):
        """
        Devuelve el nombre de la imagen en función del nombre del objecto
        y su sequencia
        """
        template = self.product_tmpl_id
        name = template.public_name if template.public_name else template.name
        return super(GalleryImageTemplate, self).compute_name_image(name=name)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    gallery_ids = fields.One2many('product_template.gallery_image',
                                  'product_tmpl_id')

    def write(self, cr, uid, ids, vals, context=None):
        r = super(ProductTemplate, self).write(cr, uid, ids, vals, context)
        update_sequences_gallery(self, cr, uid, ids, 'gallery_ids',
                                 'product_template.gallery_image')
        return r
