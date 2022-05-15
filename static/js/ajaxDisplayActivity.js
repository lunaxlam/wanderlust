'use strict';

// Retrieve data for a place_id already in the database and then display on itinerary page

fetch('/api/saved_activities')
    .then((response) => response.json())
    .catch(() => {
        alert('Something wrong with the route!')
    })
    .then((data) => {

        for (const i in data) {

            console.log(data[i]["dates"])

            document.querySelector('#saved_place').insertAdjacentHTML(
                'beforeend',
                `<section>
                    <ul>Name: ${data[i]["activity_name"]} </ul>
                    <ul>Date: ${data[i]["dates"]}</ul> 
                    <ul>Start: ${data[i]["start"]} </ul> 
                    <ul>End: ${data[i]["end"]} </ul>   
                    <ul>Location: ${data[i]["results"]["name"]} </ul>                    
                    <ul>Address: <a href='${data[i]["results"]["url"]}'>${data[i]["results"]["formatted_address"]}</a></ul>
                    <ul>Phone: ${data[i]["results"]["formatted_phone_number"]} </ul>
                    <ul>Notes: ${data[i]["notes"]} </ul>
                </section><br>`
            )
        }
    })
    .catch(() => {
        alert('Something wrong with dataset!')
    });