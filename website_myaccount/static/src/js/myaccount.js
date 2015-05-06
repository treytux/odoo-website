(function () {
    'use strict';

    openerp.website.ready().done(function() {
        $('#myaccount-profile').on('submit', function(event){
            event.preventDefault();
            var data = {name: $('#name').val() }

            if($('#email-current').val() != $('#email').val()){
                var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
                if($('#email').val().length == 0){
                    alert('Please fill email field');
                    $('#email').focus();
                    return;
                } else if($('#email-confirm').val() != $('#email').val()){
                    alert('The email address don\'t match!');
                    $('#email-confirm').focus();
                    return;
                } else if(!filter.test($('#email').val())){
                    alert('You have entered an invalid email address!');
                    $('#email').focus();
                    return;
                } else {
                    data['email'] = $('#email').val();
                }
            }

            if($('#password').val().length != 0){
                if($('#password').val() != $('#password-confirm').val()){
                    alert('Password don\'t match!');
                    $('#password-confirm').val('');
                    $('#password-confirm').focus();
                    return;
                } else {
                    data['password'] = $('#password').val();
                }
            }

            openerp.jsonRpc('/myaccount/profile/update', 'call', {
                data: data
            }).then(function(result) {
                console.log(result);
                if(result['result'] == true){
                    location = '/myaccount';
                }
            });
        });


    });
})();
