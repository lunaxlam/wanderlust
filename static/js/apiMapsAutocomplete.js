'use strict';

// Display map based on API data that is displayed at route("/.../<place_id>/details")

function initMap() {
    
    fetch('/api/saved_activities')
        .then((response) => response.json())
        .then((activities) => {

            initAutocomplete()

            const map = new google.maps.Map(document.querySelector('#map'),{
                center: {
                    lat: activities[0]['results']['geometry']['location']['lat'],
                    lng: activities[0]['results']['geometry']['location']['lng'],
                },
                scrollwheel: true,
                zoom: 12,
            });

            for (const activity in activities) {

                const lat = activities[activity]['results']['geometry']['location']['lat']
                const lng = activities[activity]['results']['geometry']['location']['lng']
                const place_name = activities[activity]['results']['name']
                const place_address = activities[activity]['results']['formatted_address']
                const place_url = activities[activity]['results']['url']

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
                        lat: lat,
                        lng: lng,
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
            }
        })
        .catch(() => {
            alert(`Oops! Something went wrong. Please contact the developer.`); 
        });

}

let autocomplete;

function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('autocomplete'),
        {
            types: ['establishment'],
            // componentRestrictions: {'country': ['AU']},
            fields: ['place_id', 'geometry', 'name']
        }
    );

    autocomplete.addListener('place_changed', onPlaceChanged);
}

// Callback function that defines what happens when an autocomplete prediction is clicked
function onPlaceChanged() {

    // Get place information on the prediction that was selected
    const place = autocomplete.getPlace();

    // Check if the selected prediction is a valid place
    if (!place.geometry) {

        document.getElementById('autocomplete').placeholder =
        'Enter a place';
    } else {

        document.querySelector('#autocomplete-mount').insertAdjacentHTML(
            'beforeend',
            `<input type='hidden' name='autocomplete' value='${place.place_id}'>`
        )

    }
}