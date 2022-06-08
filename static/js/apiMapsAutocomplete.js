'use strict';

function initMap() {
    
    fetch('/api/saved_activities')
        .then((response) => response.json())
        .catch(() => {
            alert('Oh no! The Google API trial period has ended for this application.')
        })
        .then((activities) => {

            initAutocomplete()

            const mount = document.querySelector('#saved-map');

            if ('0' in activities) {

                mount.hidden = false;

                const map = new google.maps.Map(mount,{
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
                    `<h1 class="infoWindow main-heading text-center">${place_name}</h1>` +
                    `<div class="infoWindow">` +
                    `<p class="text-center">${place_address}</p>` +
                    `<p class="text-center"><a href="${place_url}" target="_blank">View on Google Maps</a></p>` +
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
            }
        })
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