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

{
    'name': 'Website Sale Products Nav',
    'category': 'website',
    'summary': 'Permite ordenar los listados de productos de la tienda online '
               'por secuencia [defecto], precio y nombre.',
    'version': '0.1',
    'description': """
    """,
    'author': 'Trey',
    'depends': [
        'product',
        'website_sale',
        'website_sale_products_per_page',
    ],
    'data': [
        'views/product_categories.xml',
        # data
        # security
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        # 'views/product.xml',
        # 'views/product_template_gallery_image.xml',
        # 'views/product_product_gallery_image.xml',
        # 'views/product_public_category.xml',
    ],
    'demo': [
        # 'data/products.xml',
    ],
    'test': [
        # 'test/test.yml',
    ],
    'qweb': [
        # 'static/src/xml/*.xml',
    ],
    'js': [
    ],
    'css': [
    ],
    'installable': True,
}
