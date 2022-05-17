'use strict';

// A function to generate and return a queryString
function buildQueryString(evt) {

    const clicked_button = evt.target

    const type = clicked_button.getAttribute('name')

    const Inputs = {
        type: `${type}`,
        name: document.querySelector(`#${type}-select`).value
    }

    const queryString = new URLSearchParams(Inputs).toString()

    return queryString
}


// A function to execute a fetch request
function fetchItineraryBy(queryString) {

    fetch(`/api/itineraries/by_location?${queryString}`)
        .then((response) => response.json())
        .then((data) => {

            const mount = document.querySelector('#all-itineraries')
            
            mount.innerHTML = ``

            for (const i in data) {

                const itinerary_id = data[i]['itinerary_id']
                const itinerary_name = data[i]['itinerary_name']

                mount.insertAdjacentHTML(
                    'beforeend',
                    `<ul><a href='/itinerary/${itinerary_id}' target='blank'>Itinerary ID: ${itinerary_id}, ${itinerary_name}</a></ul>`
                )
            }    
        })
}



// Display itineraries by locale
const localeBtn = document.querySelector('#locale-btn')

localeBtn.addEventListener('click', (evt) => {
    evt.preventDefault();

    const queryString = buildQueryString(evt)

    fetchItineraryBy(queryString)
})


// Display itineraries by territory
const territoryBtn = document.querySelector('#territory-btn')

territoryBtn.addEventListener('click', (evt) => {
    evt.preventDefault();

    const queryString = buildQueryString(evt)

    fetchItineraryBy(queryString)
})


// Display itineraries by country
const countryBtn = document.querySelector('#country-btn')

countryBtn.addEventListener('click', (evt) => {
    evt.preventDefault();

    const queryString = buildQueryString(evt)

    fetchItineraryBy(queryString)
})