'use strict';

// Mount form to add activity

const addBtn = document.querySelector('#add-destination');

addBtn.addEventListener('click', (evt) => {

    const clicked_button = evt.target;
    const itinerary_id = clicked_button.getAttribute('name');

    addBtn.hidden = true;


    document.querySelector('#add-destination-form').insertAdjacentHTML(
        'beforeend',
        `<br />
        <h2>Add Destination</h2>
        <form action='/itinerary/${itinerary_id}/add_destination' class='active-form'>
            <label for='destination-locale'>Locale:</label>
            <input type='text' name='locale' id='destination-locale' required>
            <br>
            <label for='destination-territory'>Territory</label>
            <input type='text' name='territory' id='destination-territory' required>
            <br>
            <label for='destination-country'>Country</label>
            <input type='text' name='country' id='destination-country' pattern='(\\b\\w{3}\\b)' required>
            <br>
            <p class='hint'>Country code must be entered as three-letter 
                <a href='https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3' 
                    target='_blank'>ISO-3166</a> code standard. Need a 
                <a href='/countries' target='_blank'>hint</a>?</p>
            <input type='submit' name='submit'>
        </form>`
    )
})