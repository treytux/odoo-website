# -*- coding: utf-8 -*-
##############################################################################
#
#    Trey, Kilobytes de Soluciones
#    Copyright (C) 2014-Today Trey, Kilobytes de Soluciones (<http://www.trey.es>).
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
from openerp import tools, SUPERUSER_ID
from openerp.osv import fields, orm
from openerp.tools.translate import _
from openerp.tools.mail import plaintext2html
from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
from datetime import datetime

import logging
_log = logging.getLogger(__name__)


class Ratings(orm.Model):
    _name = "website_ratings.ratings"
    _columns = {
        'website_id': fields.many2one('website', string="Website"),

        'object_id': fields.integer(u'Id del modelo', select=True),
        'object_model': fields.char(u'Nombre del modelo', size=255, translate=False),
        'numbers_of_ratings': fields.integer(u'Número de valoraciones hechas sobre el modelo'),
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
        'object_model': fields.char(u'Nombre del modelo', size=255, translate=False),
        'date_rating': fields.datetime(u'Fecha de la valoración'),
        'rating': fields.float(u'Valoración sobre el objeto del usuario'),
    }
    _defaults = {
        'date_rating': lambda *a: datetime.now(),
    }
