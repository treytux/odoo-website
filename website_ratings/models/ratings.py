# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp import models, api, fields
import logging

# from openerp.osv import fields, orm
# from datetime import datetime

_log = logging.getLogger(__name__)


class Ratings(models.Model):
    _name = "website_ratings.ratings"

    website_id = fields.Many2one(
        comodel_name='website',
        string="Website"
    )
    object_id = fields.Integer(
        string=u'Id del modelo',
        select=True
    )
    object_model = fields.Char(
        string=u'Nombre del modelo',
        size=255,
        translate=False
    )
    numbers_of_ratings = fields.Integer(
        string=u'Número de valoraciones hechas sobre el modelo',
        default=1
    )
    ratings = fields.Float(
        string=u'Valoración media del objecto',
        default=0
    )


class UserRatings(models.Model):
    _name = "website_ratings.user_rating"

    website_id = fields.Many2one(
        comodel_name='website',
        string="Website"
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="User id"
    )
    object_id = fields.Integer(
        string=u'Id del modelo',
        select=True
    )
    object_model = fields.Char(
        string=u'Nombre del modelo',
        size=255,
        translate=False
    )
    date_rating = fields.Datetime(
        string=u'Fecha de la valoración',
        default=fields.Datetime.now()
    )
    rating = fields.Float(
        string=u'Valoración sobre el objeto del usuario'
    )
