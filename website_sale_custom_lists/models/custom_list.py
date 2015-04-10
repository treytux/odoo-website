# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp import api, models, fields


class CustomList(models.Model):
    _name = 'custom.list'
    _description = 'Custom list'

    name = fields.Char(
        string='Name',
        required=True
    )
    line_ids = fields.One2many(
        comodel_name='custom.list.line',
        inverse_name='custom_list_id',
        string='Lines'
    )


class CustomListLine(models.Model):
    _name = 'custom.list.line'
    _description = 'Custom list line'

    name = fields.Char(
        string='Empty'
    )
    custom_list_id = fields.Many2one(
        comodel_name='custom.list',
        string='Custom list'
    )
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product template'
    )
