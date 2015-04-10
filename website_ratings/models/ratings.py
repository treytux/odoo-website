# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp.osv import fields, orm
from datetime import datetime

import logging
_log = logging.getLogger(__name__)


class Ratings(orm.Model):
    _name = "website_ratings.ratings"
    _columns = {
        'website_id': fields.many2one('website', string="Website"),

        'object_id': fields.integer(u'Id del modelo', select=True),
        'object_model': fields.char(u'Nombre del modelo', size=255,
                                    translate=False),
        'numbers_of_ratings': fields.integer(u'Número de valoraciones hechas '
                                             u'sobre el modelo'),
        'ratings': fields.float(u'Valoración media del objecto'),
    }
    _defaults = {
        'numbers_of_ratings': 1,
        'ratings': 0,
    }


class UserRatings(orm.Model):
    _name = "website_ratings.user_rating"
    _columns = {
        'website_id': fields.many2one('website', string="Website"),
        'user_id': fields.many2one('res.users', string="User id"),

        'object_id': fields.integer(u'Id del modelo', select=True),
        'object_model': fields.char(u'Nombre del modelo', size=255,
                                    translate=False),
        'date_rating': fields.datetime(u'Fecha de la valoración'),
        'rating': fields.float(u'Valoración sobre el objeto del usuario'),
    }
    _defaults = {
        'date_rating': lambda *a: datetime.now(),
    }
