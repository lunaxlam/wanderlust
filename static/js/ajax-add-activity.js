'use strict';

// Retrieve data for a place_id that is currently under search

fetch('/api/search_place_data')
    .then((response) => response.json())
    .then((data) => {
        const place_name = data["name"]
        const place_address = data["address"]
        const place_url = data["place_url"]

        document.querySelector('#search_place').innerHTML =
        `<ul>${place_name}</ul>` +
        `<ul>${place_address}</ul>` +
        `<ul><a href="${place_url}" target="_blank">View on Google Maps</a></ul>`
    })
    .catch(() => {
        alert('Something went wrong!');
    });
