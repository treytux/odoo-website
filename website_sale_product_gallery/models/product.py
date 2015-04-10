# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp import models, fields, api
from openerp.addons.website_sale_product_gallery.models.gallery_image \
    import update_sequences_gallery

import logging

_log = logging.getLogger(__name__)


class GalleryImageProduct(models.Model):
    _inherit = "gallery_image"
    _name = "product_product.gallery_image"
    _description = "Gallery Image for product.product"

    product_id = fields.Many2one('product.product', u'Product')

    @property
    def object_relation_name(self):
        return "product_id"

    def compute_name_image(self, name=None, sequence=None):
        """
        Devuelve el nombre de la imagen en función del nombre del objecto
        y su sequencia
        """
        template = self.product_id.product_tmpl_id
        name = template.public_name if template.public_name else template.name

        attributes_values = [l for l in self.product_id.attribute_value_ids
                             if l.attribute_id.affects_image]
        for av in attributes_values:
            name += u'-{}-{}'.format(av.attribute_id.name, av.name)

        return super(GalleryImageProduct, self).compute_name_image(name=name)


class ProductProduct(models.Model):
    _inherit = "product.product"

    variant_gallery_ids = fields.One2many(
        'product_product.gallery_image', 'product_id')
    is_variant_gallery_visible = fields.Boolean(
        compute='_compute_is_variant_gallery_visible')

    def write(self, cr, uid, ids, vals, context=None):
        r = super(ProductProduct, self).write(cr, uid, ids, vals, context)
        update_sequences_gallery(self, cr, uid, ids,
                                 'variant_gallery_ids',
                                 'product_product.gallery_image')
        return r

    @api.one
    @api.depends('attribute_value_ids')
    def _compute_is_variant_gallery_visible(self):
        self.is_variant_gallery_visible = False

        # comprobamos que los attributos que tiene afectan las imagenes
        for att in self.attribute_value_ids:
            if att.attribute_id.affects_image:
                self.is_variant_gallery_visible = True
                break
