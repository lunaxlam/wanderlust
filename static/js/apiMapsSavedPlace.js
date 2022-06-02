'use strict';

function initMap() {
    
    fetch('/api/saved_activities')
        .then((response) => response.json())
        .then((activities) => {

            const mount = document.querySelector('#saved-map');
            mount.hidden = false;

            const map = new google.maps.Map(document.querySelector('#saved-map'),{
                center: {
                    lat: activities[0]['results']['geometry']['location']['lat'],
                    lng: activities[0]['results']['geometry']['location']['lng'],
                },
                scrollwheel: false,
                zoom: 14,
            });

            const infoWindow = new google.maps.InfoWindow();

            for (const activity in activities) {

                const lat = activities[activity]['results']['geometry']['location']['lat']
                const lng = activities[activity]['results']['geometry']['location']['lng']
                const place_name = activities[activity]['results']['name']
                const place_address = activities[activity]['results']['formatted_address']
                const place_url = activities[activity]['results']['url']

                const contentString = 
                `<h1 class="infoWindow main-heading">${place_name}</h1>` +
                `<div id="bodyContent" class="infoWindow">` +
                `<p>${place_address}</p>` +
                `<p><a href="${place_url}" target="_blank">View on Google Maps</a></p>` +
                `</div>`;

                const placeMarker = new google.maps.Marker({
                    position: {
                        lat: lat,
                        lng: lng,
                    },
                    map: map,
                });

                placeMarker.addListener('click', () => {
                    infoWindow.setContent(contentString);
                    infoWindow.open({
                        anchor: placeMarker,
                        map: map,
                        shouldFocus: false,
                    });
                });
            }
        })
}