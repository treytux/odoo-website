(function () {
    'use strict';
    $(document).ready(function () {
        function gallery(product_id, sizes, callback) {
            // console.log(product_id.val());
            console.debug("LOADING GALLERY. Product", product_id);

            openerp.jsonRpc('/shop/product/images', 'call', {
                'product_id': product_id,
                'sizes': sizes
            }).then(function(result) {
                callback(result);
            });
        }

        function print_gallery(result) {
            console.debug("RESULT", result);

            var images = result['images'];
            var nombre_producto = result['product'];

            $('.product-gallery').html('');
            if (images.length > 0) {
                $.each(images, function(i, item) {
                    // console.debug(item);
                    if(i > 0) {
	                    $('.product-gallery').append(
	                        '<a href="' + item['original'] + '" title="' + nombre_producto + '" data-gallery="data-gallery">' +
	                            '<img src="' + item['50x50'] + '" alt="' + nombre_producto + '">' +
	                        '</a>'
	                    );
                    } else {
	                    $('.product-image').html(
	                        '<a href="' + item['original'] + '" title="' + nombre_producto + '" data-gallery="data-gallery" class="product-image-default">' +
	                            '<img src="' + item['400x400'] + '" alt="' + nombre_producto + '" class="img img-responsive product_detail_img">' +
	                        '</a>'
	                    );
                    }
                });
                // $('.big_gallery').attr('src', images[0]['400x350']);
                // $('.gallery_help_not_found').addClass('hidden');
            } else {
                // $('.big_gallery').attr('src', '/website_sale_disk_images/static/src/img/not-found.png');
                console.log('Imagen no encontrada.');
                // if (result['name']) {
                //     $('.gallery_help_not_found').removeClass('hidden');
                //     $('.gallery_help_not_found').find('.name').html(result['name']);
                //     $('.gallery_help_not_found').find('.path').html(result['path']);
                //     // console.debug($('.gallery_help_not_found').find('.name'));
                // }
            }
        }

        // Cargar la galería por defecto
    	var product_id = $('input.product_id');
        if (product_id.val()) {
            gallery(product_id.val(), [[50, 50], [400, 400]], print_gallery);
        } else {
            console.debug("no hay product id");
        }

        $('.oe_website_sale').each(function () {
            var oe_website_sale = this;

            $(oe_website_sale).on('change', 'input.js_variant_change, select.js_variant_change', function (ev) {
                // var ul = $(this).parents('ul.js_add_cart_variants:first');
                // var parent = ul.closest('.js_product');
                // var product_id = parent.find('input.product_id').first();
            	var product_id = $('input.product_id');
                if (product_id.val()) {
                    gallery(product_id.val(), [[50, 50], [400, 400]], print_gallery);
                } else {
                    console.debug("no hay product id");
                }
            });
        });
    });
})();
