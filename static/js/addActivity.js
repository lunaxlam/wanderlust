'use strict';

// Mount form to add activity

const addBtn = document.querySelector('#add-activity');

addBtn.addEventListener('click', (evt) => {

    const clicked_button = evt.target;

    const itineraryID = clicked_button.getAttribute('name');
    const placeID = clicked_button.getAttribute('value');
    const lat = clicked_button.getAttribute('data-value1');
    const long = clicked_button.getAttribute('data-value2');

    document.querySelector('#add-activity-form').insertAdjacentHTML(
        'beforeend',
        `<form action='/itinerary/${itineraryID}/${placeID}/add_activity'>
            <label for='activity-name'>Name of Activity:</label>
            <input type='text' name='name' id='activity-name' required><br>
            <label for='activity-start'>Start:</label>
            <input type='datetime-local' name='start' id='activity-start'><br>
            <label for='activity-end'>End:</label>
            <input type='datetime-local' name='end' id='activity-end'><br>
            <label for='activity-notes'>Notes:</label>
            <textarea name='notes' id='activity-notes'></textarea><br>
            <input type='submit' name='submit'>
        </form>`
    )
})