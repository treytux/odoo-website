# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.
from openerp import models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    order = 'sequence'
