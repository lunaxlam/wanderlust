'use strict';

// Mount form to add activity

const addBtn = document.querySelector('#add-destination');

addBtn.addEventListener('click', (evt) => {

    const clicked_button = evt.target;
    const itinerary_id = clicked_button.getAttribute('name');

    if (document.querySelector('#add-destination-form').innerHTML === '') {

        document.querySelector('#add-destination-form').insertAdjacentHTML(
            'beforeend',
            `<form class='row g-3' action='/itinerary/${itinerary_id}/add_destination' method='POST'>
                <div class='col-md-12'>
                    <label for='destination-name' class='form-label'>Locale</label>
                    <input type='text' class='form-control' name='locale' id='destination-locale' required>
                </div>
                <div class='col-md-12'>
                    <label for='destination-territory' class='form-label'>Territory</label>
                    <input type='text' class='form-control' name='territory' id='destination-territory' required>
                </div>
                <div class='col-md-12'>
                    <label for='destination-country' class='form-label'>Country</label>
                    <input type='text' class='form-control' name='country' id='destination-country' pattern='(\\b\\w{3}\\b' required>
                    <p class='hint'>Country code must be entered as three-letter 
                        <a href='https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3' 
                            target='_blank'>ISO-3166</a> code standard. Need a 
                        <a href='/countries' target='_blank'>hint</a>?
                    </p>
                </div>
                <div class='col-12'>
                    <button type='submit' class='btn btn-primary'>Submit</button>
                </div>
            </form>`
        )
    } else {

        document.querySelector('#add-destination-form').innerHTML = '';

    }

})