'use strict';

// Display map based on API data that is displayed at route("/.../<place_id>/details")

function initMap() {

    fetch('/api/itinerary_destinations')
        .then((response) => response.json())
        .catch(() => {
            alert('Oh no! The Google API trial period has ended for this application.')
        })
        .then((destinations) => {

            const place_lat = destinations[0]["results"][0]["geometry"]["location"]["lat"];
            const place_lng = destinations[0]["results"][0]["geometry"]["location"]["lat"];
            let formatted_address = destinations[0]["results"][0]["formatted_address"];

            const map = new google.maps.Map(document.querySelector('#my-map'),{
                center: {
                    lat: place_lat,
                    lng: place_lng,
                },
                scrollwheel: false,
                zoom: 2,
                styles: [
                    {
                        'featureType': 'water',
                        'stylers': [
                            {'color': '#fCf5E5'} 
                        ]
                    }, {
                        'featureType': 'landscape.natural.landcover',
                        'stylers': [
                            {'color': '#ebd5b3'}
                        ]
                    }, {
                        'featureType': 'landscape.natural.terrain',
                        'stylers': [
                            {'color': '#f2e3cc'}
                        ]
                    },
                ],
            });
            
            const infoWindow = new google.maps.InfoWindow();

            const image = "/static/images/mapmarkerwanderlustblue.png";

            for (const destination in destinations ) {

                formatted_address = destinations[destination]["results"][0]["formatted_address"];

                const contentString = 
                `<h1 class="infoWindow main-heading">${formatted_address}</h1>`;

                const placeMarker = new google.maps.Marker({
                    position: {
                        lat: destinations[destination]["results"][0]["geometry"]["location"]["lat"],
                        lng: destinations[destination]["results"][0]["geometry"]["location"]["lng"],
                    },
                    title: `${formatted_address}`,
                    icon: {
                        url: image,
                        scaledSize: new google.maps.Size(40, 40),
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