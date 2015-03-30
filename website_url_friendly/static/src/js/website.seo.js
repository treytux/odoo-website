
/**
 *  Copyright (C) 2015 Benito Roríguez (http://b3ni.es) <brarcos@gmail.com>
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

(function () {
    'use strict';

    var website = openerp.website;
    website.add_template_file('/website_url_friendly/static/src/xml/website.seo.xml');

    website.seo.HtmlPage = website.seo.HtmlPage.extend({
        changeUrl: function (url) {
            this.url_slug = url;
        },
        url: function() {
            var url = window.location.href;
            var hashIndex = url.indexOf('#');

            if (this.url_slug) {
                var urlslug = window.location.protocol + '//' + window.location.host + '/' + this.url_slug;
                // if (hashIndex > 0)
                //     urlslug += url.substring(0, hashIndex);
                return urlslug
            } else {
                return hashIndex >= 0 ? url.substring(0, hashIndex) : url;
            }
        },
    });

    website.seo.Slugs = openerp.Widget.extend({
        template: 'website_url_friendly.slug_input',
        events: {
            'closed.bs.alert': 'destroy',
        },
        init: function(seo, slugs) {
            this.seo = seo;
            this.slugs = slugs;
            this._super();
        },
        start: function () {
            var self = this;

            self._super();
            self.$('button').on("click", function (ev) {
                var slug_div = $(this).closest('div.lang'),
                    lang = $(slug_div).data('lang'),
                    slug_now = $(slug_div).find('input').data('slug_now'),
                    slug = $(slug_div).find('input').val(),
                    loading = $(slug_div).find('.slug-loading'),
                    ok = $(slug_div).find('.slug-ok');

                if (slug_now == slug) {
                    $(slug_div).find('input').data('slug_now', slug);
                    $(slug_div).find('input').val(slug);
                    $(ok).removeClass('hide');
                    $(loading).addClass('hide');
                    return;
                }

                $(ok).addClass('hide').html(' Valid');
                $(loading).removeClass('hide');
                self.check(slug, lang).then(function (slug_check) {
                    //$(slug_div).find('input').data('slug_now', slug_check);
                    $(slug_div).find('input').val(slug_check);
                    $(ok).removeClass('hide');
                    $(loading).addClass('hide');
                }).fail(function () {
                    $(ok).removeClass('hide').html('Error!!!');
                    $(loading).addClass('hide');
                });
            });
        },
        check: function(slug, lang) {
            var self = this,
                def = $.Deferred(),
                obj = self.seo.getMainObject();

            if (!obj) {
                def.reject();
                return def;
            }

            if (slug) {
                $.getJSON("/website_url_friendly/compute_slug", {
                    'slug': slug,
                    'model': obj.model,
                    'id': obj.id,
                    'lang': lang,
                }, function(resp) {
                    def.resolve(resp.slug);
                });
            } else {
                def.resolve('');
            }

            return def;
        },
        check_all: function(slug_checked, divs_slugs, def) {
            var self = this,
                def = (typeof def == 'undefined') ? $.Deferred() : def;

            if (typeof divs_slugs == 'undefined') {
                divs_slugs = [];
                self.$('div.lang').each(function(i, d) {
                    divs_slugs.push(d);
                });

            }
            if (divs_slugs.length == 0) {
                def.resolve(true);
            } else {
                var div = divs_slugs.pop(),
                    lang = $(div).data('lang'),
                    now = $(div).find('input').data('slug_now'),
                    s = $(div).find('input').val();

                if (s == now) {
                    self.check_all(slug_checked, divs_slugs, def);
                } else {
                    self.check(s, lang).then(function(slug_check) {
                        slug_checked.push({'lang': lang, 'slug': slug_check});
                        self.check_all(slug_checked, divs_slugs, def);
                    });
                }
            }

            return def;
        },
    });

    website.seo.Configurator = website.seo.Configurator.extend({
        init: function(parent, options) {
            var self = this;
            self._super(parent, options);

            self.slug_widget = null;
            self.events['keyup input[name=slug]'] = 'slugChanged';
        },
        loadSlug: function() {
            var self = this,
                obj = this.getMainObject(),
                $input = self.$('input[name=slug]'),
                def = $.Deferred(),
                path = $('html').data('slug-path');

            if (path == '/' || path == '/page/homepage') {
                self.$el.find('.slug-form').addClass('hide');
                def.reject();
                return def;
            }

            if (!obj) {
                self.$el.find('.slug-form').addClass('hide');
                def.reject();
                return def;
            }
            var data = {'path': path, 'model': obj.model, 'model_id': obj.id};

            $.getJSON("/website_url_friendly/load", data, function(resp) {
                if (resp['empty']) {
                    self.$el.find('.slug-form').addClass('hide');
                    def.reject();
                } else {
                    //console.debug("slugs", resp);
                    self.$el.find('.seo_slugs').html('');
                    self.slug_widget = new website.seo.Slugs(self, resp['slugs']);
                    self.slug_widget.appendTo(self.$el.find('.seo_slugs'));
                }
            });

            return def;
        },
        saveSlug: function() {
            var self = this,
                obj = self.getMainObject(),
                def = $.Deferred(),
                $input = self.$('input[name=slug]'),
                slug = $input.val(),
                slug_now = $input.data('slug_now'),
                path = $('html').data('slug-path'),
                slug_checked = [];

            self.slug_widget.check_all(slug_checked).then(function() {

                $.getJSON("/website_url_friendly/save_slugs", {
                    'path': path,
                    'model': obj.model,
                    'id': obj.id,
                    'slugs': JSON.stringify(slug_checked),
                }, function(resp) {
                    if (resp['action'] == 'none')
                        return def.resolve(true);
                    else if (resp['action'] == 'home')
                        return window.location = '/';
                    else if (resp['action'] == 'error')
                        return alert("ERROR SLUG: " + resp['msg']);
                    else {
                        var location = '/';
                        $.each(resp.slugs, function(i, s) {
                            if (s[1] == self.lang_default)
                                location = '/' + s[0];
                        });
                        window.location = location;
                    }
                });
            }).fail(function () { def.reject(); });

            return def;
        },
        slugChanged: function () {
            var self = this;
            setTimeout(function () {
                var url = self.$('input[name=slug][data-lang_default=true]').val();
                self.htmlPage.changeUrl(url);
                self.renderPreview();

                // var url = self.htmlPage.url();
                // var title = self.$('input[name=seo_page_title]').val();
                // console.debug();
                // self.htmlPage.changeTitle(title);
            }, 0);
        },
        // renderPreview: function () {
        //     var preview = new website.seo.Preview(this, {
        //         title: this.htmlPage.title(),
        //         description: this.htmlPage.description(),
        //         url: this.htmlPage.url(),
        //     });
        //     var $preview = this.$('.js_seo_preview');
        //     $preview.empty();
        //     preview.appendTo($preview);
        // },

        // inherit
        loadMetaData: function () {
            var self = this,
                def = $.Deferred();

            self._super().then(function(data) {
                $.getJSON("/website_url_friendly/langs", {}, function(resp) {
                    self.langs = resp;
                    self.lang_default = null;

                    $.each(self.langs, function (i, l) {
                        if (l.default)
                            self.lang_default = l.lang;
                    })

                    self.loadSlug().then(function(data_slug) {
                        def.resolve(data);
                    }).fail(function () { def.reject(); });
                });
            }).fail(function () { def.reject(); });

            return def;
        },
        saveMetaData: function(data) {
            var self = this,
                def = $.Deferred();

            self._super(data).then(function(res) {
                self.saveSlug().then(function(res_slug) {
                    def.resolve(res);
                }).fail(function () { def.reject(); });
            }).fail(function () { def.reject(); });

            return def;
        },

    });

})();
