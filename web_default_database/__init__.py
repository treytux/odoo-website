# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.
from openerp import http, tools
import logging
_log = logging.getLogger(__name__)

if tools.config.get('db_default', None):
    dbs = http.dispatch_rpc("db", "list", [True])
    if tools.config['db_default'] in dbs:
        _log.info('default database: %s' % tools.config['db_default'])

        def db_monodb(httprequest=None):
            return tools.config['db_default']

        http.db_monodb = db_monodb
    else:
        _log.error(
            'Default database %s not exists!!!' % tools.config['db_default'])
else:
    _log.info('Default database not set, add "db_default" to config file')
