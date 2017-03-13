'use strict';

(function ($) {

    $(function () {

        $.get('/api/v2/officers').done(function (data) {
            console.log(data)
        });

        $('#chart-container').orgchart({
            'data': '/api/v2/officers',
            'depth': 10,
            'nodeContent': 'title'
        });

    });


})(jQuery);