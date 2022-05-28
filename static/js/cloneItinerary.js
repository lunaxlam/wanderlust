'use strict';

// Mount form to clone trip

const addBtn = document.querySelector('#clone-trip');

addBtn.addEventListener('click', (evt) => {

    const clicked_button = evt.target;

    const itinerary_id = clicked_button.getAttribute('name');

    if (document.querySelector('#clone-trip-form').innerHTML === '') {

        document.querySelector('#clone-trip-form').innerHTML =
        `<br />
        <form action='/itinerary/${itinerary_id}', method='POST'>
            <label for='itinerary-name'>Name Your Trip: </label>
            <input type='text' name='name' id='itinerary-name' required>
            <br>
            <label for='itinerary-overview'>Overview: </label>
            <input type='text' name='overview' id='itinerary-overview' required>
            <br>
            <input type='submit' name='submit'>
        </form>
        <br />`

    } else {

        document.querySelector('#clone-trip-form').innerHTML = ''

    }

})