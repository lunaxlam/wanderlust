'use strict';

// Mount form to clone trip

const addBtn = document.querySelector('#clone-trip');

addBtn.addEventListener('click', (evt) => {

    const clicked_button = evt.target;

    const itinerary_id = clicked_button.getAttribute('name');

    if (document.querySelector('#clone-trip-form').innerHTML === '') {

        document.querySelector('#clone-trip-form').innerHTML =
        `<form class='row g-3 filter' action='/itinerary/${itinerary_id}' method='POST'>
                <div class='col-md-12'>
                    <label for='itinerary-name' class='form-label'>Name Your Trip</label>
                    <input type='text' class='form-control' name='name' id='itinerary-name' required>
                </div>
                <div class='col-md-12'>
                    <label for='itinerary-overview' class='form-label'>Overview</label>
                    <input type='text' class='form-control' name='overview' id='itinerary-overview' required>
                </div>
                <div class='col-12'>
                    <button type='submit' class='btn btn-secondary btn-sm'>Submit</button>
                </div>
            </form>`

    } else {

        document.querySelector('#clone-trip-form').innerHTML = ''

    }

})