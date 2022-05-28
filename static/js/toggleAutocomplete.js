'use strict';

// Event Listeners to toggle Autocomplete Search Btn

const autocompleteBtn = document.querySelector('#autocomplete-btn');
const autocompleteForm = document.querySelector('#display-autocomplete-form');

autocompleteBtn.addEventListener('click', () => {

    if (autocompleteForm.style.display === "") {
        autocompleteForm.style.display = "block";

    } else {
        autocompleteForm.style.display = "";
    }

})
