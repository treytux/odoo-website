document.addEventListener('DOMContentLoaded', function(){
    jQuery(document).ready(function($){
        // Validate form
        $('form[action="/crm/contactus"]').on('submit', function(e) {
            // Validate privacy_policy is checked
            if(!$('input[name="privacy_policy"]').is(':checked')) {
                e.preventDefault();  // Prevent form from submitting
                alert('Es obligatorio aceptar la Política de Privacidad.');
            }
        });
    });
});
