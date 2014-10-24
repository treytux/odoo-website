# -*- coding: utf-8 -*-
##############################################################################
#
#    Trey, Kilobytes de Soluciones
#    Copyright (C) 2014-Today Trey, Kilobytes de Soluciones (<www.trey.es).
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


class product_feature_line(models.Model):
    _name = "product.feature.line"

    name = fields.Char(u'Empty', translate=True)
    product_tmpl_id = fields.Many2one('product.template', u'Template product')
    feature_id = fields.Many2one('product.template.feature',
                                 u'Feature')
    value_ids = fields.Many2many(comodel_name='product.template.feature.value',
                                 relation='product_template_feature_value_rel',
                                 column1='line_id',
                                 column2='val_id')


class product_template_feature(models.Model):
    _name = "product.template.feature"

    name = fields.Char(u'Name', required=False, translate=True, select=True,
                       help=u'Feature name')
    parent_id = fields.Many2one('product.template.feature', u'Parent')
    value_ids = fields.One2many('product.template.feature.value', 'feature_id',
                                u'Valores')


class product_template_feature_value(models.Model):
    _name = "product.template.feature.value"

    name = fields.Char(u'Name', required=False, translate=True, select=True,
                       help=u'Feature value name')
    feature_id = fields.Many2one('product.template.feature', u'Feature')
