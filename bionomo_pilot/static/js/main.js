function main() {
    (function(){
        if($('#ads-form-wapper .field-error').length == 0 && $('#ads-form-wapper .field-info').length == 0){
            $("#ads-form-wapper").addClass("hidden");
        }

        $("#ads-link").click(function(event){
            event.preventDefault();
            $(this).toggleClass('active')
            $("#ads-form-wapper").toggleClass("hidden");
        });

        $("#languages > div.hide-text a").hover(
            function(){
                $(this).parent().removeClass("hide-text");
                $(this).parent().addClass("show-text");
            },
            function(){
                $(this).parent().removeClass("show-text");
                $(this).parent().addClass("hide`-text");
            }
        );

        if (typeof $().numericInput == 'function') {
            $(".field .float-input").numericInput({allowFloat: true, allowNegative: true, min:-180, max: 180});
        }

        if ( typeof $.typeahead == 'function' ) {
            $.typeahead({
                input: '.main-search-input',
                minLength: 0,
                order: "asc",
                dynamic: true,
                delay: 500,
                backdrop: {
                    "background-color": "#fff"
                },
                template: function (query, item) {

                    var color = "#777";
                    if (item.status === "owner") {
                        color = "#ff1493";
                    }
                    return '<span class="row">{{scientific_name}}</span>'
                },
                emptyTemplate: $("#msg_no_collections").text() + "{{query}}",
                source: {
                    user: {
                        display: "scientific_name",
                        href: "{{url}}",

                        ajax: {
                            "url": "/async/scientific_name/{{query}}/" + $("#locale").text()
                        }
                    }
                },
                callback: {
                    onClick: function (node, a, item, event) {

                        window.location.href =[ selectedName ]+"";
                    },
                    onSendRequest: function (node, query) {
                        console.log('request is sent')
                    },
                    onReceiveRequest: function (node, query) {
                        console.log('request is received')
                    }
                },
                debug: true
            });
            setTimeout(function(){$('.main-search-input').focus();}, 10);
        }

        $("#the_coder_content").slideUp( "fast", function() {});
        $(".developer-name").hover(
            function(){
                var el = $("#the_coder_content");
                if (!el.hasClass("sliding")){
                    el.addClass("sliding");
                    el.delay(300).slideDown( 250, function() {
                        el.removeClass("sliding");
                    });
                }
            },
            function(){
                var el = $("#the_coder_content");
                if (!el.hasClass("sliding")){
                    el.addClass("sliding");
                    el.delay(1500).slideUp( 250, function() {
                        el.removeClass("sliding");
                    });
                }
            }
        );
        $("#the_coder_ref").click(function(event){
            event.preventDefault();

            var el = $("#the_coder_content");
            if (!el.hasClass("sliding")){
                    el.addClass("sliding");
                    el.delay(100).slideToggle( 250, function() {
                        el.removeClass("sliding");
                    });
                }

        });

        $("#result-options .links-wrapper .links .map").removeClass("hidden");
        $("#result-options .links-wrapper .links .map").click(function(event){
            event.preventDefault();

            if ($("#maps").hasClass("map-hidden")) {
                $("#maps").removeClass("map-hidden");
                $("#maps").addClass("map-extending");
                $("#maps").animate({'height': '450px'}, 500, "linear", function () {
                    google.maps.event.trigger(myMap(), 'resize');
                    $("#maps").removeClass("map-extending");
                    $("#maps").addClass("map-shown");
                });
            } else if ($("#maps").hasClass("map-shown")) {
                $("#maps").removeClass("map-shown");
                $("#maps").addClass("map-extending");
                $("#maps").animate({'height': '0px'}, 500, "linear", function () {
                    google.maps.event.trigger(myMap(), 'resize');
                    $("#maps").removeClass("map-extending");
                    $("#maps").addClass("map-hidden");
                });
            }
        });

        if ( typeof $().select2 == 'function' ) {
            $(".select-field").select2({
                placeholder: $("#msg_click_to_select").text()
            });
        }

        function myMap() {
            if (document.getElementById("maps") !=  null) {

                NhmatandaLocation = {
                    'lat': -19.302483,
                    'long': 34.269221
                };
                var latLong = new google.maps.LatLng(-19.302483, 34.269221);
                var mapProp= {
                    center:latLong,
                    zoom:5
                };

                map = new google.maps.Map(document.getElementById("maps"), mapProp);

                var markers = $("#maps1 .coordinates").map(function(coordinate, index){
                    _lat = parseFloat($(this).find(".latitude").text());
                    _long = parseFloat($(this).find(".longitude").text());
                    return new google.maps.Marker({
                        map: map,
                        icon: {
                            path: google.maps.SymbolPath.CIRCLE,
                            scale: 3,
                            strokeColor: '#670f44'
                        },
                        position: {lat: _lat, lng: _long}
                    });
                });

                var markerCluster = new MarkerClusterer(map, markers,
                    {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});

                return map;
            }
        }

        $("#result-list .list-item").each(function(index){
            var link = $(this).find(".item .classification_tree_lnk");
            var title = $(this).find(".title").html();
            var classification_tree = $(this).find(".classification-tree").html();
            $(this).find(".clas_tree").html('');

            $(link).flyout({
                content: classification_tree,
                title: title,
                html: true,
                trigger: 'manual'
            }).mouseover(function() {
                $(this).flyout('show');
            }).mouseout(function() {
                $(this).flyout('hide');
            });
        });

    }());
}
main();
