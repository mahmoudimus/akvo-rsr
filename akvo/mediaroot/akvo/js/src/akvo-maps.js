/*jslint browser: true*/
/*global $, jQuery, Handlebars, google*/

(function () {
    "use strict";

    // When included akvo-maps.js will query the page for elements with
    // class ".akvo_map". These elements should be generated by the maps
    // Django template tag. Each map element will have a div element and
    // a JavaScript literal with data which are used to create a map with
    // corresponding locations from the RSR API
    // There are currently three kinds of maps:
    //      "static" is used on the RSR home page where we want a world map with small markers
    //      "small" is used for the single object maps for projects and organisations
    //      "dynamic" are the large all-object maps for projects and organisations

    var addMap, addPin, populateMap, mapOptions, prepareNextRequest, getResourceUrl;


    // For each .akvo_map element on the page, read options
    // and kick of the creation of a new map
    $(document).ready(function () {
        $('.akvo_map').each(function () {
            var mapId = $(this).attr('id');
            addMap({
                mapId: mapId,
                mapElement: document.getElementById(mapId),
                mapOpts: window[mapId]
            });
        });
    });


    // Creates the map with options and makes the initial AJAX request
    addMap = function (map) {
        $(map.mapElement).gmap(mapOptions(map.mapOpts.type)).bind('init', function () {
            // use $.ajax to be able to setup jsonp with a named callback, "callback",
            // and set cache: true to suppress the "_=<random number>" query string variable jQuery adds by default
            $.ajax({
                url: getResourceUrl(map),
                dataType: "jsonp",
                jsonp: 'callback',
                jsonpCallback: 'callback',
                cache: true,
                success: function(data) {
                    populateMap(map, data);
                }
            });
        });
    };


    // Creates resource URLS based on map options
    getResourceUrl = function (map) {
        var opts, url, limit;
        opts = map.mapOpts;
        // call /api/v1/map_for_project/ or /api/v1/map_for_organisation/ resources
        //TODO: derive the host from the current page URL instead maybe?
        url = opts.host + 'api/v1/' + opts.resource + '/';
        //limit = 0 means all objects. If this becomes too heavy limit can be set to get the objects in multiple chunks
        limit = 100;
        // if object_id holds a value then that's the ID of the object we want to fetch
        if (opts.object_id) {
            // if object_id holds a value then that's the ID of the object we want to fetch
            url += opts.object_id + '/?format=jsonp&depth=1';
        } else {
            // otherwise we want all objects of the resource's type
            url += '?format=jsonp&limit=' + limit;
        }
        return url;
    };

    // Populates the map with data
    populateMap = function (map, data) {
        var objects, opts, pinTmpl, addOrganisationData, addProjectData;
        opts = map.mapOpts;

        // Since API resources that list multiple objects (projects or organisations) include
        // an objects array we need to add the single project or organisation to an array. This Since
        // we want to keep using the same logic for both cases
        if (opts.object_id === "") {
            objects = data.objects;
        } else {
            objects = [data];
        }

        pinTmpl = Handlebars.compile(
            '<div class="mapInfoWindow" style="height:150px; min-height:150px; max-height:150px; overflow:hidden;">' +
                '<a class="small" href="{{url}}">{{title}}</a>' +
                '{{#if thumb}}' +
                    '<div style="text-align: center; margin-top: 5px;">' +
                        '<a href="{{url}}" title="{{title}}">' +
                            '<img src="{{thumb}}" alt="">' +
                        '</a>' +
                    '</div>' +
                '{{/if}}' +
            '</div>'
        );

        // populate the location object with data from an Organisation model object
        addOrganisationData = function (object, location) {
            location.url = object.absolute_url;
            location.title = object.name;
            try {
                location.thumb = object.logo.thumbnails.map_thumb;
            } catch (e0) { location.thumb = ''; }
            return location;
        };

        // populate the location object with data from a Project model object
        addProjectData = function (object, location) {
            location.url = object.absolute_url;
            location.title = object.title;
            try {
                location.thumb = object.current_image.thumbnails.map_thumb;
            } catch (e1) { location.thumb = ''; }
            return location;
        };

        $.each(objects, function (i, object) {
            if (opts.object_id) {
                // for single objects show all locations
                $.each(object.locations, function (k, location) {
                    //TODO: extend this for additional resource types
                    if (opts.resource === 'map_for_organisation') {
                        location = addOrganisationData(object, location);
                    } else {
                        location = addProjectData(object, location);
                    }
                    addPin(map, location, pinTmpl);
                });
            } else {
                // if we're displaying multiple objects we only show the primary locations
                var location;
                location = object.primary_location;
                if (location) {
                    if (opts.resource === 'map_for_organisation') {
                        location = addOrganisationData(object, location);
                    } else {
                        location = addProjectData(object, location);
                    }
                    addPin(map, location, pinTmpl);
                }
            }
        });

        if (opts.type === 'dynamic' || opts.type === 'static') {
            var initialLocation = new google.maps.LatLng(0.0, 0.0);
            $(map.mapElement).gmap('get', 'map').setCenter(initialLocation);
        }

        // If we are rendering multiple objects and there are more objects to
        // grab from the API
        if (isNaN(opts.object) && data.meta.next !== null) {
            prepareNextRequest(map, data.meta.next);
        }
    };

    // Add a single pin
    addPin = function (map, location, template) {
        var marker, opts;
        opts = map.mapOpts;
        marker = opts.host + 'rsr/media/core/img/';

        // get a custom marker if there is one, otherwise it's red for organisations and blue for projects
        if (opts.marker_icon) {
            marker = marker + opts.marker_icon;
        } else if (opts.resource === 'map_for_organisation') {
            marker = marker + 'redMarker.png';
        } else {
            marker = marker + 'blueMarker.png';
        }

        if (opts.type === 'static' || opts.type === 'small') {
            // shrink the marker for "static" maps
            if (opts.type === 'static') {
                marker = new google.maps.MarkerImage(marker, null, null, null, new google.maps.Size(10.5, 17));
            }
            $(map.mapElement).gmap('addMarker', {
                'position': new google.maps.LatLng(location.latitude, location.longitude),
                'clickable': false,
                'icon': marker,
                'bounds': true
            });
            // if the map is zoomed in a lot we zoom out a bit
            if ($(map.mapElement).gmap('get', 'map').getZoom() > 8) {
                $(map.mapElement).gmap('get', 'map').setZoom(8);
            }
        // "dynamic"
        } else {
            $(map.mapElement).gmap('addMarker', {
                'position': new google.maps.LatLng(location.latitude, location.longitude),
                'icon': marker,
                'bounds': true
            }).click(function () {
                $(map.mapElement).gmap('openInfoWindow', {
                    'content': template(location)
                }, this);
            });
        }
    };


    // Since we need to update the callback parameters we don't use the meta.next
    // but create a new resource url
    prepareNextRequest = function (map, resource) {
        var url = $.url(resource),
            urlTmpl = Handlebars.compile('{{host}}{{path}}?format=jsonp&depth=1&limit={{limit}}&offset={{offset}}'),
            newUrl = urlTmpl({
                'host': url.attr('host'),
                'path': url.attr('path'),
                'limit': Number(url.param('limit')),
                'offset': Number(url.param('offset'))
            });
        $.ajax({
            url: newUrl,
            dataType: "jsonp",
            jsonp: 'callback',
            jsonpCallback: 'callback',
            cache: true,
            success: function(data) {
                populateMap(map, data);
            }
        });
    };

    mapOptions = function (mapType) {
        var options;
        // "static" and "small" are set to zoom 0 to begin with so that you see a world map until it has been populated
        // scroll wheel zoom is only enabled for the large "dynamic" maps
        if (mapType === 'static') {
            options = {
                'draggable': false,
                'mapTypeControl': false,
                'navigationControl': true,
                'scaleControl': false,
                'scrollwheel': false,
                'streetViewControl': false,
                'zoom': 0,
                'zoomControl': false //removes the (non-functional) zoom buttons
            };
        } else if (mapType === 'small') {
            options = {
                'draggable': true,
                'mapTypeControl': false,
                'navigationControl': true,
                'scaleControl': true,
                'scrollwheel': false,
                'streetViewControl': false,
                'zoom': 0
            };
        } else {
            options = {
                draggable: true,
                mapTypeControl: true,
                navigationControl: true,
                scaleControl: true,
                scrollwheel: true,
                streetViewControl: false,
                //if zoom is set to 2 (as it should) Safari/Chrome only displays part of the global map for some reason
                zoom: 3, 
                minZoom: 2

            };
        }
        return options;
    };
}());
