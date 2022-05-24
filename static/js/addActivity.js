'use strict';

// Mount form to add activity

const addBtn = document.querySelector('#add-activity');

addBtn.addEventListener('click', (evt) => {

    const clicked_button = evt.target;

    const itinerary_id = clicked_button.getAttribute('name');
    const place_id = clicked_button.getAttribute('value')

    document.querySelector('#add-activity-form').insertAdjacentHTML(
        'beforeend',
        `<form action='/itinerary/${itinerary_id}/${place_id}/add_activity'>
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