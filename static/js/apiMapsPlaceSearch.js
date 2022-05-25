'use strict';

// Display map based on API data that is displayed at route("/.../<place_id>/details")

function initMap() {

    fetch('/api/search_place_data')
        .then((response) => response.json())
        .then((data) => {

            const place_lat = data["location"]["lat"];
            const place_lng = data["location"]["lng"];
            const place_name = data["name"];
            const place_address = data["address"];
            const place_url = data["place_url"];

            const map = new google.maps.Map(document.querySelector('#map'),{
                center: {
                    lat: place_lat,
                    lng: place_lng,
                },
                scrollwheel: true,
                zoom: 14,
            });

            const contentString = 
            `<h1 id="firstHeading" class="infoWindow">${place_name}</h1>` +
            `<div id="bodyContent" class="infoWindow">` +
            `<p>${place_address}</p>` +
            `<p><a href="${place_url}" target="_blank">View on Google Maps</a></p>` +
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
            alert(`Oops! Something went wrong. Please contact the developer.`); 
        });

}