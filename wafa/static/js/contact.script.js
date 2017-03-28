$(function () {

    var msg = '<div style="width: 300px;">' +
        '<h4 style="margin-bottom: 8px;">Hi, we\'re<span> WAFA FERTILIZER</span></h4>' +
        '<p class="nobottommargin">Our mission is to establish an environment for the <strong>availability </strong> and ' +
        '<strong>optimal</strong> use of quality fertilizer for West African producers. We Contribute to the development of' +
        ' <strong>regional agricultural policies </strong> ' +
        ' in terms of agronomy, infrastructure, taxation and financing in the transparency and general interest for the  ' +
        '<strong>development of agriculture</strong>.</p>' +
        '</div>';

    $('#google-map').gMap({
        address: city,
        maptype: 'ROADMAP',
        zoom: 14,
        markers: [
            {
                lat: -12.043333,
                lng: -77.028333,
                address: city,
                html: msg,
                icon: {
                    image: marker,
                    iconsize: [32, 39],
                    iconanchor: [32, 39]
                }
            }
        ],
        doubleclickzoom: false,
        controls: {
            panControl: true,
            zoomControl: true,
            mapTypeControl: true,
            scaleControl: false,
            streetViewControl: false,
            overviewMapControl: false
        }
    });


    var $fromSection = $('.contact-widget');

    var element = $($fromSection),
        elementAlert = element.attr('data-alert-type'),
        elementLoader = element.attr('data-loader'),
        elementResult = element.find('.contact-form-result'),
        elementRedirect = element.attr('data-redirect');

    element.find('form').submit(function (e) {
        e.preventDefault();
    }).validate({
        submitHandler: function (form) {
            if (grecaptcha.getResponse()) {
                elementResult.hide();
                $(form).find('.form-process').fadeIn();
                $(form).ajaxSubmit({
                    target: elementResult,
                    dataType: 'json',
                    success: function (data) {
                        if (elementLoader === 'button') {
                            defButton.html(defButtonText);
                        } else {
                            $(form).find('.form-process').fadeOut();
                        }
                        if (data.alert !== 'error' && elementRedirect) {
                            window.location.replace(elementRedirect);
                            return true;
                        }
                        if (elementAlert === 'inline') {
                            var alertType = 'alert-success';
                            if (data.alert === 'error') {
                                alertType = 'alert-danger';
                            }
                            elementResult.removeClass('alert-danger alert-success').addClass('alert ' + alertType).html(data.message).slideDown(400);
                        } else {
                            elementResult.attr('data-notify-type', data.alert).attr('data-notify-msg', data.message).html('');
                            SEMICOLON.widget.notifications(elementResult);
                        }
                        if ($(form).find('.g-recaptcha').children('div').length > 0) {
                            grecaptcha.reset();
                        }
                        if (data.alert !== 'error') {
                            $(form).clearForm();
                        }
                    }
                });
            }
            return false;

        }
    });

});


