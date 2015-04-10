# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp import models, api, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    in_stock = fields.Boolean(
        compute='_compute_in_stock',
        string='In stock',
        readonly=True,
        default=False
    )

    @api.one
    def _compute_in_stock(self):
        self.in_stock = True and self.sudo().qty_available > 0 or False
