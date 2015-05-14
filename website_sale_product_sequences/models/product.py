# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.
from openerp import models, fields


class Product(models.Model):
    _inherit = "product.product"
    order = 'website_sequence_product'

    website_sequence_product = fields.Integer(string='Product Sequence')
