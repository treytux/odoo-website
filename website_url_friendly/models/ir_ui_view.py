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

import logging

from openerp import models
from openerp.addons.website.models import website
from openerp.addons.web.http import request

logger = logging.getLogger(__name__)


def url_for(path_or_uri, lang=None):
    url = website.url_for(path_or_uri, lang)

    if url in ('', '/', '/web'):
        return url

    if url.startswith('http'):
        return url

    for sw in ('/web/', '/web#', '/usr/', 'mailto', '#'):
        if url.startswith(sw):
            return url

    IrHttp = request.registry['ir.http']
    return IrHttp.url_for(url)


class UiView(models.Model):
    _name = "ir.ui.view"
    _inherit = "ir.ui.view"

    def render(self, cr, uid, id_or_xml_id, values=None, engine='ir.qweb',
               context=None):
        if values is None:
            values = {}
        values['url_for'] = url_for

        return super(UiView, self).render(cr, uid, id_or_xml_id, values,
                                          engine, context)
