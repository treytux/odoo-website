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

from openerp import models, fields


class Slug(models.Model):
    _name = 'website_url_friendly.slug'

    name = fields.Char(string=u"Slug", required=True, translate=True)
    path = fields.Char(string=u"Path", required=True, translate=False)
    model = fields.Char(string=u"Model", required=True, translate=False)
    model_id = fields.Integer(string=u"Model ID", required=True)

    _sql_constraints = [
        ('name_unique', 'unique (name)', u'The slug must be unique !'),
        ('path_unique', 'unique (path)', u'The path must be unique !'),
    ]
