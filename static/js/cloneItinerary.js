'use strict';

// Mount form to add activity

const addBtn = document.querySelector('#clone-trip');

addBtn.addEventListener('click', (evt) => {

    const clicked_button = evt.target;

    const itinerary_id = clicked_button.getAttribute('name');

    document.querySelector('#clone-trip-form').insertAdjacentHTML(
        'beforeend',
        `<br />
        <form action='/itinerary/${itinerary_id}', method='POST'>
            <label for='itinerary-name'>Itinerary Name: </label>
            <input type='text' name='name' id='itinerary-name' required>
            <br>
            <label for='itinerary-overview'>Overview: </label>
            <input type='text' name='overview' id='itinerary-overview' required>
            <br>
            <input type='submit' name='submit'>
        </form>
        <br />`
    )
})