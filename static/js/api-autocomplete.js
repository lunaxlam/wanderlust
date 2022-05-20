'use strict'

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

        document.querySelector('#autocomplete-place-id').insertAdjacentHTML(
            'beforeend',
            `<input type='hidden' name='autocomplete' value='${place.place_id}'><br>
            <input type="submit" value="Submit">`
        )

    }
}