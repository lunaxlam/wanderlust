'use strict';

// Event Listener to hide create new itinerary if user toggles

const hideBtn = document.querySelector('#hide-create');
const trips = document.querySelector('#mount-itinerary');

hideBtn.addEventListener('click', () => {

    if (trips.style.display === "none") {
        trips.style.display = "block";
    } else {
        trips.style.display = "none";
    }

})