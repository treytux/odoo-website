# -*- coding: utf-8 -*-
import datetime
import hashlib
import logging
import re
import traceback
import werkzeug
import werkzeug.routing
from werkzeug._compat import wsgi_decoding_dance

import openerp
from openerp.addons.base import ir
from openerp.addons.base.ir import ir_qweb
from openerp.addons.website.models.website import slug, url_for
from openerp.http import request
from openerp.osv import orm

logger = logging.getLogger(__name__)


class ir_http(orm.AbstractModel):
    _inherit = 'ir.http'

    # def _find_handler(self, return_rule=False):
    #     try:
    #         return super(ir_http, self)._find_handler(return_rule=return_rule)
    #     except werkzeug.exceptions.NotFound:
    #         handler = self._find_custom_handler()
    #         if handler is None:
    #             raise  # 404 default
    #         return handler  # custom

    # def _find_custom_handler(self):

    #     # def _get_wsgi_string(name):
    #     #     val = request.httprequest.environ.get(name)
    #     #     if val is not None:
    #     #         return wsgi_decoding_dance(val, self._routing_map.charset)

    #     path_info = request.httprequest.path

    #     logger.info("Handler not found: <{}>".format(path_info))
    #     return request.redirect(path + '?' + request.httprequest.query_string)

    #     #return self.routing_map().bind_to_environ(request.httprequest.environ).match(return_rule=return_rule)

    # def _dispatch(self):
    #     try:
    #         self._find_handler()
    #     except werkzeug.exceptions.NotFound:
    #         path_info = request.httprequest.path
    #         logger.info("Handler not found: <{}>".format(path_info))

    #         logger.info("URL FRIENDLY {} ==> {}".format(path_info, '/page/pepe'))
    #         return self.reroute('/page/pepe')

    #     return super(ir_http, self)._dispatch()

    # def routing_map(self):
    #     routing = super(ir_http, self).routing_map()

    #     if not hasattr(self, '_customs_routing_map'):
    #         logger.info("Adding customs routes...")
    #         self._customs_routing_map = []
    #         logger.info(self._routing_map)

    #     return routing
