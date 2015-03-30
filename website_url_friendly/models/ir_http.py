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
import openerp
import werkzeug
import unicodedata
import re

from urlparse import urlparse
from openerp.http import request
from openerp.osv import orm
from openerp.tools import ustr

logger = logging.getLogger(__name__)


def slugify_friendly(s):
    s = ustr(s)
    if s[0] == u'/':
        s = s[1:]
    if s[-1] == u'/':
        s = s[0:-1]

    uni = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    slug = re.sub('[\W_]', ' ', uni).strip().lower()
    slug = re.sub('[-\s]+', '-', slug)

    if len(slug) == len(s):
        pos = [m.start() for m in re.finditer('/', s)]
        if len(pos) == 0:
            return slug

        slug = list(slug)
        for i in pos:
            slug[i] = s[i]

        slug = u"".join(slug)
        if slug[0] == u'/':
            slug = slug[1:]

    return slug


class SlugManager(orm.AbstractModel):
    _inherit = 'ir.http'

    _cache_expresions = {}
    _NOT_VALID_SLUG_NAMES = ['logo.png', 'web', 'longpolling', 'usr']
    _NOT_VALID_SLUG_PATH = [u'/', u'/page/homepage', u'/page/themes']

    def _dispatch(self):
        try:
            self._find_handler()
            r = super(SlugManager, self)._dispatch()
            return r
        except werkzeug.exceptions.NotFound:
            pass

        rerouting = hasattr(request, "rerouting") and \
            len(request.rerouting) > 0
        if rerouting:
            return super(SlugManager, self)._dispatch()

        website = request.registry['website'].get_current_website(
            request.cr, request.uid, context=request.context)
        langs = [lg[0] for lg in website.get_languages()]

        path_info, lang = self.extract_slug(request.httprequest.path, website,
                                            langs)
        if path_info in SlugManager._NOT_VALID_SLUG_NAMES:
            return super(SlugManager, self)._dispatch()

        response = self.find_slug(path_info, lang, website.default_lang_code)
        if response is None:
            return super(SlugManager, self)._dispatch()

        return response

    def _postprocess_args(self, arguments, rule):
        r = super(SlugManager, self)._postprocess_args(arguments, rule)
        if r and r.status_code == 301:
            o = urlparse(r.location)
            path = o.path
            return self.reroute(path)
        return r

    def _find_ids_in_path(self, exp, path):
        if exp not in SlugManager._cache_expresions:
            count = 0
            count_slug = 0
            exp_parse = unicode(exp)
            slugs = []

            while True:
                if exp_parse.find('<id>') != -1:
                    id0, id1 = 'id{}'.format(count), 'id{}'.format(count+1)
                    re_id = '([^/]*-(?P<{}>\d+))?(?P<{}>\d+)?'.format(id0, id1)
                    exp_parse = exp_parse.replace('<id>', re_id, 1)
                    count += 2
                    slugs.append((id0, id1))
                elif exp_parse.find('<slug>') != -1:
                    slug = 'slug{}'.format(count_slug)
                    re_id = '(?P<{}>[a-zA-Z0-9\-]+)'.format(slug)
                    exp_parse = exp_parse.replace('<slug>', re_id, 1)
                    count_slug += 1
                    slugs.append(slug)
                else:
                    break

            exp_parse = "^(?:/[^/]+)?{}$".format(exp_parse)
            SlugManager._cache_expresions[exp] = (slugs, re.compile(exp_parse))

        slugs, reexp = SlugManager._cache_expresions[exp]
        m = reexp.search(path)
        if not m:
            return None

        rets = []
        for part in slugs:
            if isinstance(part, tuple):
                id1 = m.group(part[0])
                id2 = m.group(part[1])

                rets.append(int(id1) if id1 else int(id2) if id2 else None)
            else:
                rets.append(m.group(part))

        return rets

    def extract_slug(self, path, website=None, langs=None):
        """ Extrae el slug de un path y tb su idioma """
        website = website or request.website
        lang_default = website.default_lang_code
        langs = langs or [lg[0] for lg in website.get_languages()]

        o = path.split('/')
        valid, lang = self.check_valid_lang(o[1], langs=langs)
        if valid:
            path = u"/" + u"/".join(o[2:])
            slug, _ = self.extract_slug(path, website, langs)
            return slug, lang
        else:
            path = u"/".join(o[1:])
            return path, lang_default

    def find_slug(self, slug, lang, lang_default):
        """ Busca un slug por su slug """
        context = request.context.copy()
        context['lang'] = lang

        Slug = request.registry['website_url_friendly.slug']

        slugs = Slug.search_read(
            request.cr, openerp.SUPERUSER_ID,
            [('name', '=', slug)],
            ['name', 'path', 'model_id', 'model'], context=context)

        if len(slugs) > 0:
            # hay slug
            path = slugs[0]['path']
            request.lang = lang
            request.context['lang'] = lang

            if lang != lang_default:
                path = u"/{}{}".format(lang, path)

            # print "SLUG DISPATCH [{} {}] {} => {}".format(
            #     lang, lang_default, slug, path)

            # request.httprequest.environ['PATH_INFO'] = path
            # return self._dispatch()

            # if request.httprequest.query_string:
            #     path += '?' + request.httprequest.query_string

            return self.reroute(path)

        return None

    def check_valid_lang(self, lang, langs=None):
        langs = langs or [lg[0] for lg in website.get_languages()]

        if lang in langs:
            return True, lang

        return False, lang

        # if len(lang) != 2:
        #     return False, lang

        # langs_short = [lg for lg in langs if lg.startswith(lang)]
        # if len(langs_short) > 0:
        #     return True, langs_short[0]
        # else:
        #     return False, lang

    def check_valid_slug(self, slug, website, langs=None):
        langs = langs or [lg[0] for lg in website.get_languages()]
        path = u"/" + slug
        path, lang = self.extract_slug(path, website, langs)

        if path in SlugManager._NOT_VALID_SLUG_NAMES:
            return False

        if not self.check_valid_lang(lang, langs=langs):
            return False

        return True

    def compute_slug(self, slugtext, model, id, lang):
        """ Devuelve un nombre de slug único """
        def _add_prefix(txt):
            txt_parts = txt.split('-')
            prefix = 1
            if len(txt_parts) > 1 and txt_parts[-1].isdigit():
                prefix = int(txt_parts[-1]) + 1
                txt_parts = u"-".join(txt_parts[0:-1])
            elif len(txt_parts) > 1:
                txt_parts = u"-".join(txt_parts)
            else:
                txt_parts = u"".join(txt_parts)
            return u"{}-{}".format(txt_parts, prefix)

        context = request.context.copy()
        context['lang'] = lang

        # routes registers
        urls = self.routing_map().bind_to_environ(request.httprequest.environ)
        if urls.test(slugtext):
            return self.compute_slug(_add_prefix(slugtext), model, id, lang)

        # slugs registrados
        Slug = request.registry['website_url_friendly.slug']
        slugs = Slug.search(request.cr, openerp.SUPERUSER_ID,
                            [('name', '=', slugtext)], context=context)
        if len(slugs) > 0:
            return self.compute_slug(_add_prefix(slugtext), model, id, lang)

        return slugtext

    def url_for(self, url):
        """ URL ODOO => SLUG """
        Slug = request.registry['website_url_friendly.slug']

        o = urlparse(url)
        path = o.path

        def _find_slug(slug, lang):
            context = request.context.copy()
            context['lang'] = lang

            slugs = Slug.search_read(request.cr, openerp.SUPERUSER_ID,
                                     [('path', '=', slug)], ['name'],
                                     context=context)
            if len(slugs) == 0:
                return None

            # print "   URLFOR FOUND", lang, slug, slugs

            if lang != request.website.default_lang_code:
                url = u'/{}/{}'.format(lang, slugs[0]['name'])
            else:
                url = u'/{}'.format(slugs[0]['name'])

            if o.query:
                url += u'?{}'.format(o.query)

            if o.fragment:
                url += '#' + o.fragment

            return url

        _, lang = self.extract_slug(path, website=request.website)

        # buscamos slug
        compute_path = self.compute_path(path)
        slug_found = _find_slug(compute_path, lang)

        if slug_found:
            return slug_found

        # por defecto
        return url

    def compute_path(self, path):
        """ Procesa la url de odoo antes de guardar el slug """
        if path.find('/page/') == -1:
            return path

        ids = self._find_ids_in_path('/page/<slug>', path)
        if ids:
            return u"/page/{}".format(ids[0])

        ids = self._find_ids_in_path('/page/website\.<slug>', path)
        if ids:
            return u"/page/{}".format(ids[0])

        # raise Exception(u"SlugManager: url no parseable {}".format(path))
        return path
