'use strict';

// Display itineraries

const localeBtn = document.querySelector('#locale-btn')

localeBtn.addEventListener('click', (evt) => {
    evt.preventDefault();

    fetch('/api/itineraries/by_locale')
        .then((response) => response.json())
        .catch(() => {
            alert('Something wrong with the route!')
        })
        .then((data) => {

            for (const i in data) {

            console.log(data[i])
            document.querySelector('#all-itineraries').innerHTML = 

            data[i]

            }
           
        })
})