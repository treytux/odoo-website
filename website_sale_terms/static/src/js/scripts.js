document.addEventListener('DOMContentLoaded', function(){
    jQuery(document).ready(function($){
        $('form[action="/shop/confirm_order"]').on('submit', function(e) {
            // Validate checkout_policy is checked
            if(!$('input[name="checkout_policy"]').is(':checked')) {
                e.preventDefault();  // Prevent form from submitting
                alert('Es obligatorio aceptar las Condiciones de Venta y la Política de Privacidad.');
            }
        });
    });
});
