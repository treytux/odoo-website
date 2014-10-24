(function () {
    'use strict';

    var _t = openerp._t,
        website = openerp.website;

    //website.add_template_file('/website_ratings/static/src/xml/ratings.xml');

    openerp.website.Rating = openerp.Widget.extend({
        //template: "website_ratings.base",

        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            var self = this;

            self.object_id = self.$el.parent().data('object_id');
            self.object_model = self.$el.parent().data('object_model');
            self.rating_name = self.$el.parent().data('input_name');

            self.$el.parent().find('ul').attr('name', self.rating_name);
            self.el_ratings = self.$el.parent().find("li.star-rating");
            self.span_number_ratings = self.$el.parent().find("li.star-rating-count");

            self.ratings = 0;
            self.numbers_of_ratings = 0;
            self.send_rating = false;

            openerp.jsonpRpc('/ratings/read', 'call', {
                object_model: self.object_model,
                object_id: self.object_id,
            }).then(function(result) {
                if (result.ratings)
                    self.ratings = result.ratings;
                if (result.numbers_of_ratings)
                    self.numbers_of_ratings = result.numbers_of_ratings;
                if (result.send_rating)
                    self.send_rating = result.send_rating;

                self.update_rating();
                self.$el.parent().find('a').on('click', function(event) {
                    event.preventDefault();
                    // console.debug($(this));
                    var rating = $(this).data('star');
                    self.event_send_rating(rating);
                });

            });

            self._super();
        },
        update_rating: function () {
            var self = this;
            var rating = Math.round(self.ratings);

            self.el_ratings.removeClass('star-rating-on');
            if (rating > 0) {
                for(var i=0; i<=5; i++) {
                    if (i <= rating) {
                        var input = self.el_ratings[i-1];
                        $(input).addClass('star-rating-on');
                    }
                }
            }
            self.span_number_ratings.html('(' + self.numbers_of_ratings + ')');
        },
        event_send_rating: function(rating) {
            var self = this;
            if (self.send_rating)
                return;

            openerp.jsonRpc('/ratings/send', 'call', {
                'rating': rating,
                'object_model': self.object_model,
                'object_id': self.object_id,
            }).then(function(result) {
                if (result['error'])
                    return;

                self.send_rating = true;
                self.ratings = result.ratings;
                self.numbers_of_ratings = result.numbers_of_ratings;
                self.update_rating();
            });
        },
    });

    openerp.website.ready().done(function() {
        $('div.ratings').each(function() {
            new openerp.website.Rating().appendTo($(this));
        });
    });
})();
