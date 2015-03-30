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

import json
import logging

from openerp.http import request
from openerp.addons.web import http
from openerp.addons.website_url_friendly.models.ir_http import slugify_friendly

logger = logging.getLogger(__name__)


class UrlFrindly(http.Controller):
    def _parse_slug(self, slug):
        return slugify_friendly(slug.strip())

    def _langs(self):
        default_lang_code = request.website.default_lang_code
        all_langs = request.website.get_languages()

        return default_lang_code, all_langs

    @http.route(['/website_url_friendly/langs'],
                type='http', auth="user", website=True)
    def get_langs(self):
        default, alls = self._langs()
        data = [{'lang': lg[0], 'default': lg[0] == default}
                for lg in alls]
        return json.dumps(data)

    @http.route(['/website_url_friendly/load'],
                type='http', auth="user", website=True)
    def load_slug(self, path, model, model_id):
        Slug = request.registry['website_url_friendly.slug']
        IrHttp = request.registry['ir.http']

        # comprobamos que el path sea sluggeable
        if path in request.registry['ir.http']._NOT_VALID_SLUG_PATH:
            return json.dumps({'empty': True})

        # leemos slugs por idioma
        path_new = IrHttp.compute_path(path)
        print "load", model, path_new
        slug_id = Slug.search(request.cr,
                              request.uid, [('path', '=', path_new)])

        context = request.context.copy()
        default_lang_code = request.website.default_lang_code

        data = []
        for lg in request.website.get_languages():
            lang = lg[0]
            context['lang'] = lang

            if len(slug_id) > 0:
                slug = Slug.read(request.cr, request.uid, slug_id[0],
                                 ['name'], context)
                name = slug['name']
            else:
                name = u''

            data.append({'lang': lang,
                         'lang_default': lang == default_lang_code,
                         'name': name})

        return json.dumps({'empty': False, 'slugs': data})

    @http.route(['/website_url_friendly/compute_slug'],
                type='http', auth="user", website=True)
    def compute_slug(self, slug, model, id, lang):
        IrHttp = request.registry['ir.http']

        slug = self._parse_slug(slug)
        if not IrHttp.check_valid_slug(slug, request.website):
            slug += "-1"

        compute = IrHttp.compute_slug(slug, model, id, lang)
        data = {'slug': compute, 'model': model, 'id': id, 'lang': lang}
        return json.dumps(data)

    @http.route(['/website_url_friendly/save_slugs'],
                type='http', auth="user", website=True)
    def save_slugs(self, slugs, path, model, id):
        Slug = request.registry['website_url_friendly.slug']
        IrHttp = request.registry['ir.http']
        context = request.context.copy()
        default_lang, langs = self._langs()
        id = int(id)

        # comprobamos si el modelo soporta slugs
        if path in request.registry['ir.http']._NOT_VALID_SLUG_PATH:
            return json.dumps({'empty': True})

        # find if exists slug
        path = IrHttp.compute_path(path)
        slug_ids = Slug.search(request.cr,
                               request.uid, [('path', '=', path)])

        # validez de los idiomas
        slugs = json.loads(slugs)
        for slug in slugs:
            if slug['lang'] not in [l[0] for l in langs]:
                return json.dumps({'action': 'error',
                                   'msg': u"Lang not valid"})

        # comprobamos si borramos
        hay_slugs = len([s for s in slugs if s['slug'] == u'']) == 0
        if len(slug_ids) > 0 and not hay_slugs:
            Slug.unlink(request.cr, request.uid, [slug_ids[0]])
            # Model.write(request.cr, request.uid, [id], {'slug_id': False})
            return json.dumps({'action': 'home'})

        # primero el idioma por defecto
        for slug in slugs:
            for i, l in enumerate(langs):
                if l[0] == slug['lang']:
                    slug['id'] = i
        slugs.sort(key=lambda s: s['id'])

        # guardamos en los lenguajes indicados
        return_slugs = []
        for slug in slugs:
            name = self._parse_slug(slug['slug'])
            lang = slug['lang']
            context['lang'] = lang

            name = IrHttp.compute_slug(name, model, id, lang)

            data = {'name': name, 'path': path, 'model': model,
                    'model_id': id}

            if len(slug_ids) == 0:
                slug_id = Slug.create(request.cr, request.uid, data,
                                      context=context)
                slug_ids = [slug_id]
            else:
                Slug.write(request.cr, request.uid, slug_ids, data,
                           context=context)

            return_slugs.append((name, lang))

        if len(return_slugs) == 0:
            return json.dumps({'action': 'none'})
        else:
            return json.dumps({'action': 'reload', 'slugs': return_slugs})
