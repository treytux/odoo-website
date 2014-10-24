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

import os
import base64
import fnmatch
import cStringIO
from openerp import fields, api, tools, _
from openerp.osv import osv
from openerp.addons.website.models.website import slugify
from PIL import Image

import logging
_log = logging.getLogger(__name__)


class GalleryImage(osv.AbstractModel):
    _name = "gallery_image"
    _description = "Gallery Image"

    _order = 'sequence'
    _sql_constraints = [('name_uniq', 'unique(name)', _(u"El nombre debe ser único!"))]

    def _last_update_default(self):
        """ Devuelve la fecha actual """
        return fields.Datetime.now()

    name = fields.Char(u'Image', required=False)
    sequence = fields.Integer(u'Sequence', required=True, store=True)
    image = fields.Binary(u'Image File', required=True, store=False, compute='_comput_image', inverse='_inverse_image')
    image_path = fields.Char(u'Image Path')
    src = fields.Char(u'URL imagen', store=True, compute='_compute_src')
    last_update_img = fields.Datetime(u'Fecha modificacion', default=_last_update_default)

    def _get_next_sequence(self, cr, uid, object_relation_id=None):
        """ Devuelve el siguiente valor para la sequence """
        object_relation_id = self.object_relation.id if not object_relation_id else object_relation_id
        return self.search(cr, uid, [(self.object_relation_name, '=', object_relation_id)], count=True) + 1

    @api.one
    @api.depends('image_path')
    def _compute_src(self):
        self.src = False
        if self.image_path:
            self.src = u'/images/{}'.format(self.name)

    @api.one
    @api.depends('image_path')
    def _comput_image(self):
        self.image = False

        if self.image_path:
            # leemos imagen
            if not os.path.exists(self.image_path):
                return

            with open(self.image_path, 'rb') as f:
                self.image = base64.b64encode(f.read())

    @api.one
    @api.depends('name', 'sequence', 'image_path')
    def _inverse_image(self):
        # comprobamos directorio de gallery
        path = os.path.join(tools.config.filestore(self.env.cr.dbname), 'product_gallery')
        if not os.path.exists(path):
            os.makedirs(path)

        # nombre del fichero
        name_file = self.compute_name_image()

        # salvamos path
        path = os.path.join(path, name_file)
        img = Image.open(cStringIO.StringIO(base64.b64decode(self.image)))
        img.save(path)

        # with open(path, 'w') as ofile:

        #     ofile.write(base64.b64decode(self.image))

        self.write({'image_path': path, 'name': name_file})

    @property
    def object_relation_name(self):
        raise NotImplementedError()

    @property
    def object_relation(self):
        if not hasattr(self, self.object_relation_name):
            raise NotImplementedError(u"No existe el campo {}".format(self.object_relation_name))
        return getattr(self, self.object_relation_name)

    def compute_name_image(self, name=None, sequence=None):
        """
        Devuelve el nombre de la imagen en función del nombre del objecto
        y su sequencia
        """
        name = name or self.object_relation.name
        sequence = sequence or self.sequence

        if sequence > 1:
            name_file = u"{}-{}.jpg".format(slugify(name), sequence)
        else:
            name_file = u"{}.jpg".format(slugify(name))

        return name_file

    def unlink(self, cr, uid, ids, context=None):
        for img in self.browse(cr, uid, ids, context=context):
            if not img.image_path:
                continue

            # borramos thumbnails y original
            delete_thumbails(img.image_path)
            try:
                os.remove(img.image_path)
            except:
                _log.exception(u"Error al borrar el original")

        return super(GalleryImage, self).unlink(cr, uid, ids, context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'image_path' in vals:
            for gallery in self.browse(cr, uid, ids, context=context):
                delete_thumbails(gallery.image_path)
                vals.update({'last_update_img': fields.Datetime.now()})
        return super(GalleryImage, self).write(cr, uid, ids, vals, context)

    def create(self, cr, uid, vals, context=None):
        vals['sequence'] = self._get_next_sequence(cr, uid, vals[self.object_relation_name])
        return super(GalleryImage, self).create(cr, uid, vals, context)


def delete_thumbails(image_path):
    """ Borra del disco las imagenes asociadas a este fichero con sus diferentes tamaños """
    if not image_path:
        return

    path, file_name = os.path.split(image_path)
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, file_name):
            matches.append(os.path.join(root, filename))

    # no borramos el original
    if image_path in matches:
        matches.remove(image_path)

    for f in matches:
        os.remove(f)


def update_sequences_gallery(self, cr, uid, ids, field_gallery, model_gallery):
    """ Actualiza los nombres de una galleria asociada a un object self
    en función de su sequencia """
    for obj in self.browse(cr, uid, ids):
        model_gallery = self.pool.get(model_gallery)

        fix_images = []
        for image in getattr(obj, field_gallery):
            name_compute = image.compute_name_image(image.object_relation.name, image.sequence)
            #name_compute = compute_name_image(image.object_relation.name, image.sequence)
            if name_compute != image.name:
                delete_thumbails(image.image_path)

                fix_images.append((image, name_compute))
                image.name = 'fix_{}_{}'.format(slugify(model_gallery), image.id)

                # rename
                path, file_name = os.path.split(image.image_path)
                new_image_path = os.path.join(path, image.name)
                os.rename(image.image_path, new_image_path)

        if len(fix_images):
            for image, name_compute in fix_images:
                # rename
                path, file_name = os.path.split(image.image_path)
                new_image_path = os.path.join(path, name_compute)
                os.rename(os.path.join(path, image.name), new_image_path)

                # write
                image.write({'name': name_compute, 'image_path': new_image_path})
