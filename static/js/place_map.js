'use strict';


function initMap() {

    fetch('/api/place_info')
        .then((response) => response.json())
        .then((place) => {
            const place_lat = place[0]["lat"];
            const place_lng = place[0]["lng"];
            const place_name = place[1]
            const place_address = place[2]
            const place_url = place[3]

            const map = new google.maps.Map(document.querySelector('#map'),{
                center: {
                    lat: place_lat,
                    lng: place_lng,
                },
                scrollwheel: true,
                zoom: 13,
            });

            const contentString = 
            `<div id="content">` +
            `</div>` +
            `<h1 id="firstHeading" class="infoWindow">${place_name}</h1>` +
            `<div id="bodyContent" class="infoWindow">` +
            `<p>${place_address[0]}</p>` +
            `<p>${place_address[1]}, ${place_address[2]}</p>` +
            `<p><a href="${place_url}" target="_blank">View on Google Maps</a>` +
            `</div>`;

            const infoWindow = new google.maps.InfoWindow({
                content: contentString
            });

            const placeMarker = new google.maps.Marker({
                position: {
                    lat: place_lat,
                    lng: place_lng,
                },
                map: map,
            });

            placeMarker.addListener('click', () => {
                infoWindow.open({
                    anchor: placeMarker,
                    map: map,
                    shouldFocus: false,
                });
            });
        })
        .catch(() => {
            alert(`Something went wrong. Please contact the developer.`); 
        });

}