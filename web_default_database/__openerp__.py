# -*- coding: utf-8 -*-
###############################################################################
#
#    Trey, Kilobytes de Soluciones
#    Copyright (C) 2015-Today Trey, Kilobytes de Soluciones <www.trey.es>
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
    'name': 'Default database',
    'category': 'Tool',
    'summary': 'Set a default database to Odoo a instance.',
    'version': '0.1',
    'description': '''

    Set a default database to a Odoo instance.

    Install
    =======
    Add 'db_default' option in config file openerp-server.conf and run
    "openerp-server" command with argument
    --load=web,web_kanban,web_default_database

    Enjoy
    ''',
    'author': 'Trey Kilobytes de Soluciones (www.trey.es)',
    'depends': ['base'],
    'installable': True,
}
