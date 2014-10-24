(function () {
    'use strict';

    openerp.website.ready().done(function() {
        $('.wishlist-products-add').each(function() {
            $(this).on('click', function(e) {
                e.preventDefault();
                openerp.jsonRpc('/shop/wishlist/add', 'call', {
                    'product_tmpl_id': $(this).attr('product_tmpl_id')
                }).then(function(result) {
                    if (result['error'])
                        return;
                });
            });
        });
        $('.wishlist-products-remove').each(function() {
            $(this).on('click', function(e) {
                e.preventDefault();
                openerp.jsonRpc('/shop/wishlist/remove', 'call', {
                    'wishlist_product_id': $(this).attr('wishlist_product_id')
                }).then(function(result) {
                    if (result['error'])
                        return;
                    location.reload();
                    // Las siguientes líneas nos permitirían eliminar el elemento de la lista o mostrar un mensaje de lista vacia sin recargar la página
                    // $('a[wishlist_product_id="' + result.wishlist_product_id + '"]').closest('.wishlist-product').remove();
                    // if( $('.wishlist-products .wishlist-product').length == 0 ) {
                    //     // Ocultar tabla y mostrar mensaje no hay productos en la lista
                    // }
                });
            });
        });
        $('.wishlist-products-empty').each(function() {
            $(this).on('click', function(e) {
                e.preventDefault();
                openerp.jsonRpc('/shop/wishlist/empty', 'call', {
                    'wishlist_id': $(this).attr('wishlist_id')
                }).then(function(result) {
                    if (result['error'])
                        return;
                    location.reload();
                    // Las siguientes líneas nos permitirían eliminar la lista o mostrar un mensaje de lista vacia sin recargar la página
                    // Ocultar tabla y mostrar mensaje no hay productos en la lista
                    // $('.wishlist-products').remove();
                });
            });
        });
    });
})();
