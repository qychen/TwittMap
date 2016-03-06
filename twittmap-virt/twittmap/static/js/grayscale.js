
var server_url = "http://twittmap.us-east-1.elasticbeanstalk.com/"

// jQuery to collapse the navbar on scroll
function collapseNavbar() {
    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
}

$(window).scroll(collapseNavbar);
$(document).ready(collapseNavbar);

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
  if ($(this).attr('class') != 'dropdown-toggle active' && $(this).attr('class') != 'dropdown-toggle') {
    $('.navbar-toggle:visible').click();
  }
});

// Google Maps Scripts
var map = null;
// When the window has finished loading create our google map below
google.maps.event.addDomListener(window, 'load', init);
//google.maps.event.addDomListener(window, 'resize', function() {
//    map.setCenter(new google.maps.LatLng(40.6700, -73.9400));
//});

function init() {
    // Basic options for a simple Google Map
    // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    var mapOptions = {
        // How zoomed in you want the map to start at (always required)
        zoom: 4,
        minZoom: 1,
        // The latitude and longitude to center the map (always required)
        center: new google.maps.LatLng(38.4419, -95.1419), 

    };

    // Get the HTML DOM element that will contain your map 
    // We are using a div with id="map" seen below in the <body>
    var mapElement = document.getElementById('map');

    // Create the Google Map using out element and options defined above
    map = new google.maps.Map(mapElement, mapOptions);

    map.addListener('click', surround);

}

var markers = [];
var image = '/static/img/map-marker.png';

function surround(event) {
    var latitude = event.latLng.lat();
    var longitude = event.latLng.lng();
    console.log( latitude + ', ' + longitude ); 

    var xmlhttp = new XMLHttpRequest();
    var url = server_url+"surround?lat="+event.latLng.lat()+"&long="+event.latLng.lng();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var resp = JSON.parse(xmlhttp.responseText);
            tweets = resp.hits.hits;
            console.log(tweets);
            
            for (var i = 0; i < markers.length; i++) {
                markers[i].setMap(null);
            }
            markers = [];

            var infowindow = new google.maps.InfoWindow();

            for (i=0;i<tweets.length;i++){

                //create marker and text for each point
                ts = tweets[i]._source;
                //console.log(ts.text);
                myLatLng = new google.maps.LatLng(ts.location[1], ts.location[0]);
                var marker = new google.maps.Marker({
                    position: myLatLng,
                    map: map,
                    animation: google.maps.Animation.DROP,
                });

                google.maps.event.addListener(marker, 'click', (function(marker, i) {
                    return function() {
                      contentString = '<div style="color: #333"><p>'+tweets[i]._source.username+": "+tweets[i]._source.text+'</p></div>';
                      infowindow.setContent(contentString);
                      infowindow.open(map, marker);
                    }
                })(marker, i));

                markers.push(marker);
            }

        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();

}

//add click event for keywords
$(".keyword").click(keyword);

function keyword() {

    var xmlhttp = new XMLHttpRequest();
    var url = server_url+"search?keyword="+this.text;
    //var url = server_url+"search?keyword=snow";

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var resp = JSON.parse(xmlhttp.responseText);
            tweets = resp.hits.hits;
            console.log(tweets);
            
            for (var i = 0; i < markers.length; i++) {
                markers[i].setMap(null);
            }
            markers = [];

            var infowindow = new google.maps.InfoWindow();

            for (i=0;i<tweets.length;i++){

                //create marker and text for each point
                ts = tweets[i]._source;
                //console.log(ts.text);
                myLatLng = new google.maps.LatLng(ts.location[1], ts.location[0]);
                var marker = new google.maps.Marker({
                    position: myLatLng,
                    map: map,
                    animation: google.maps.Animation.DROP,
                });

                google.maps.event.addListener(marker, 'click', (function(marker, i) {
                    return function() {
                      contentString = '<div style="color: #333"><p>'+tweets[i]._source.username+": "+tweets[i]._source.text+'</p></div>';
                      infowindow.setContent(contentString);
                      infowindow.open(map, marker);
                    }
                })(marker, i));

                markers.push(marker);
            }
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();

}


