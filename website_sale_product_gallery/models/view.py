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

import logging
from openerp.osv import osv

logger = logging.getLogger(__name__)


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
            logger.info((u"gallery --"))

            # comprobamos si teines atributos que afecten a la imagen
            att_affects_image = [a for a in obj.attribute_line_ids
                                 if a.attribute_id.affects_image]

            logger.info(att_affects_image)

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
        logger.info((u"*" * 30) + "  PRODUCT TEMPLATE " + str(template.id))
        res = [img for img in template.gallery_ids
               if len(img.attribute_value_ids) == 0]
        logger.info(res)
        logger.info((u"*" * 30))
        return res

    def _get_gallery_product_product(self, product):
        """ Buscamos las imagenes dentro de la gallery que concuerdan con la
        variante pasada """
        logger.info((u"*" * 30) + "  PRODUCT PRODUCT " + str(product.id))

        attributes_values = [l.id for l in product.attribute_value_ids
                             if l.affects_image]
        attributes_values_len = len(attributes_values)

        gallery = []
        for img in product.product_tmpl_id.gallery_ids:
            rest = set(attributes_values) - \
                set([l.id for l in img.attribute_value_ids])

            # logger.info("{}: {} - {} = {}".format(
            #     img.id,
            #     set(attributes_values),
            #     set([l.id for l in img.attribute_value_ids]),
            #     rest))

            if len(rest) != attributes_values_len:
                # alguno de los atributos casa con la imagen, lo mostramos
                gallery.append(img)

        logger.info("------")
        logger.info(gallery)
        logger.info((u"*" * 30))

        return gallery
