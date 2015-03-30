# -*- coding: utf-8 -*-

#    Copyright (C) 2015 Benito Roríguez (http://b3ni.es) <brarcos@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp.osv import orm


class SlugManager(orm.AbstractModel):
    _inherit = 'ir.http'

    def compute_path(self, path):
        if path.find('/shop/') == -1:
            return super(SlugManager, self).compute_path(path)

        ids = self._find_ids_in_path('/shop/category/<id>', path)
        if ids:
            return u"/shop/category/{}".format(ids[0])

        ids = self._find_ids_in_path('/shop/product/<id>', path)
        if ids:
            return u"/shop/product/{}".format(ids[0])

        return super(SlugManager, self).compute_path(path)
