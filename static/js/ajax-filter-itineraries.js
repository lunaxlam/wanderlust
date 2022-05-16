'use strict';

// A function to initiate a fetch request

function fetchItineraryBy(queryString) {

    fetch(`/api/itineraries/by_location?${queryString}`)
        .then((response) => response.json())
        .then((data) => {

            const mount = document.querySelector('#all-itineraries')
            
            mount.innerHTML = ``

            for (const i in data) {

                const itinerary_id = data[i]["itinerary_id"]
                const itinerary_name = data[i]["itinerary_name"]

                mount.insertAdjacentHTML(
                    'beforeend',
                    `<ul><a href="/itinerary/${itinerary_id}">${itinerary_name}</a></ul>`
                )
            }    
        })
}


const localeBtn = document.querySelector('#locale-btn')

localeBtn.addEventListener('click', (evt) => {
    evt.preventDefault();

    const Inputs = {
        type: "locale",
        name: document.querySelector('#locale-select').value
    }

    const queryString = new URLSearchParams(Inputs).toString()

    fetchItineraryBy(queryString)
})


// Display itineraries by territory

const territoryBtn = document.querySelector('#territory-btn')

territoryBtn.addEventListener('click', (evt) => {
    evt.preventDefault();

    const Inputs = {
        type: "territory",
        name: document.querySelector('#territory-select').value
    }

    const queryString = new URLSearchParams(Inputs).toString()

    fetchItineraryBy(queryString)
})


// Display itineraries by territory

const countryBtn = document.querySelector('#country-btn')

countryBtn.addEventListener('click', (evt) => {
    evt.preventDefault();

    const Inputs = {
        type: "country",
        name: document.querySelector('#country-select').value
    }

    const queryString = new URLSearchParams(Inputs).toString()

    fetchItineraryBy(queryString)
})