# -*- coding: utf-8 -*-
# License, author and contributors information in:
# __openerp__.py file at the root folder of this module.

from openerp.osv import orm


class SlugManager(orm.AbstractModel):
    _inherit = 'ir.http'

    def __init__(self, *args, **kwargs):
        super(SlugManager, self).__init__(*args, **kwargs)
        self._NOT_VALID_SLUG_PATH.append('/blog')

    def compute_path(self, path):
        if path.find('/blog/') == -1:
            return super(SlugManager, self).compute_path(path)

        ids = self._find_ids_in_path('/blog/<id>/post/<id>', path)
        if ids:
            return u"/blog/{}/post/{}".format(ids[0], ids[1])

        ids = self._find_ids_in_path('/blog/<id>/tag/<id>', path)
        if ids:
            return u"/blog/{}/tag/{}".format(ids[0], ids[1])

        ids = self._find_ids_in_path('/blog/<id>', path)
        if ids:
            return u"/blog/{}".format(ids[0])

        return super(SlugManager, self).compute_path(path)
