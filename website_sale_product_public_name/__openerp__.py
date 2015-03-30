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

{
    "name": "Website Sale Product Public Name",
    'version': '1.0',
    'category': 'Website',
    'summary': 'Add Public Name in Product Template',
    'description': """
Add field public name in product template
=========================================
    """,
    'author': 'Trey Kilobytes de Soluciones (www.trey.es)',
    'website': 'http://www.trey.es',
    'depends': [
        'website_sale',
        'website_sale_products_per_page'
    ],
    'data': [
        'views/product_view.xml'
    ],
    'demo': [
    ],
    'test': [
    ],
    'images': [
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}

