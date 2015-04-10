# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp.osv import osv


class View(osv.osv):
    _inherit = "ir.ui.view"

    def render(self, cr, uid, id_or_xml_id, values=None, engine='ir.qweb',
               context={}):
        cxn = context.copy()
        cxn.update({'get_gallery': self.gallery})

        return super(View, self).render(cr, uid, id_or_xml_id, values, engine,
                                        context=cxn)

    def gallery_tmpl(self, obj):
        return self._get_gallery_product_template(obj)

    def gallery(self, obj):
        """
        Devuelve las images de un producto.
            - Si es un product.product devuelve la galleria para esta variante
              concreta
            - Si es un product.template comprueba si tiene variantes que
              afecten a las imagenes. En este caso devuelve la primera.
              Si no, devuelve las imágnes del template.
        """
        if obj._name == 'product.template':
            # comprobamos si teines atributos que afecten a la imagen
            att_affects_image = [a for a in obj.attribute_line_ids
                                 if a.attribute_id.affects_image]
            if len(att_affects_image) > 0:
                return self._get_gallery_product_product(
                    obj.product_variant_ids[0])
            else:
                return self._get_gallery_product_template(obj)
        elif obj._name == 'product.product':
            return self._get_gallery_product_product(obj)

        return []

    def _get_gallery_product_template(self, template):
        """ Buscamos dentro de la galleria las imagenes sin atributos """
        res = [img for img in template.gallery_ids
               if len(img.attribute_value_ids) == 0]
        return res

    def _get_gallery_product_product(self, product):
        """ Buscamos las imagenes dentro de la gallery que concuerdan con la
        variante pasada """
        attributes_values = [l.id for l in product.attribute_value_ids
                             if l.affects_image]
        attributes_values_len = len(attributes_values)
        gallery = []
        for img in product.product_tmpl_id.gallery_ids:
            rest = set(attributes_values) - \
                set([l.id for l in img.attribute_value_ids])
            if len(rest) != attributes_values_len:
                # alguno de los atributos casa con la imagen, lo mostramos
                gallery.append(img)
        return gallery
