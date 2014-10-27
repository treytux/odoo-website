# -*- coding: utf-8 -*-

import logging
from openerp.addons.website.models.website import slug as slug_website
from openerp.osv import osv, orm

logger = logging.getLogger(__name__)


def slug(value):
    logger.info("PEPE")
    if isinstance(value, orm.browse_record) and hasattr(value, "_custom_slug"):
        return slug_website(value)
    return slug_website(value)


class view(osv.osv):
    _inherit = "ir.ui.view"

    # def render(self, cr, uid, id_or_xml_id, values=None, engine='ir.qweb', context=None):
    #     # overwrite slug method
    #     if values is None:
    #         values = dict()
    #     values.update({'slug': slug})

    #     return super(view, self).render(cr, uid, id_or_xml_id, values, engine, context)
