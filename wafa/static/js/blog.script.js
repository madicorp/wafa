'use strict';

(function ($, PDFJS) {

    $(function () {
        $(".document").each(function () {
            var elem = $(this), url = $(elem).attr("href");
            var reader = new FileReader();
            reader.onload = function (e) {
                var arrayBuffer = e.target.result;
                var uint8Array = new Uint8Array(arrayBuffer);
                console.log(arrayBuffer);

                PDFJS.disableTextLayer = true;
                PDFJS.getDocument(uint8Array).then(function (pdf) {
                    pdf.getPage(1).then(function (page) {
                        console.log(page);
                        var canvas = document.createElement('canvas');
                        var viewport = page.getViewport(1.0);
                        var ctx = canvas.getContext('2d');
                        var viewerWidth = 400;
                        var scale = viewerWidth / viewport.width;
                        viewport = page.getViewport(scale);
                        canvas.width = viewport.width;
                        canvas.height = viewport.height;
                        page.render({
                            canvasContext: ctx,
                            viewport: viewport
                        }).then(function () {
                            $(elem).parents(".entry-image").css("background-image", "url("+canvas.toDataURL()+")").css("background-size", "cover").removeClass("preloader");
                        });

                    });
                });
            };

            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.responseType = 'blob';
            xhr.onload = function (e) {
                if (this.status == 200) {
                    var myBlob = this.response;
                    console.log(myBlob);
                    reader.readAsArrayBuffer(myBlob);
                }
            };
            xhr.send();


        });
    });

})(jQuery, PDFJS);