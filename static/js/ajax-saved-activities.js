'use strict';

// Display saved activity

fetch('/api/saved_activities')
    .then((response) => response.json())
    .catch(() => {
        alert('Something wrong with the route!')
    })
    .then((data) => {

        for (const i in data) {

            document.querySelector('#saved-place').insertAdjacentHTML(
                'beforeend',
                `<section>
                    <ul>Name: ${data[i]["activity_name"]} </ul>
                    <ul>Dates: ${data[i]["dates"]}</ul> 
                    <ul>Start: ${data[i]["start"]} </ul> 
                    <ul>End: ${data[i]["end"]} </ul>   
                    <ul>Location: ${data[i]["results"]["name"]} </ul>                    
                    <ul>Address: <a href='${data[i]["results"]["url"]}' target='_blank'>${data[i]["results"]["formatted_address"]}</a></ul>
                    <ul>Phone: ${data[i]["results"]["formatted_phone_number"]} </ul>
                    <ul>Notes: ${data[i]["notes"]} </ul>
                    <button id="delete" value="${data[i]["activity_id"]}">Delete Activity</button>

                </section><br>`
            )            
        }

        const buttons = document.querySelectorAll('#delete');

        for (const button of buttons) {
            button.addEventListener('click', (evt) => {
                
                const clicked_button = evt.target

                const activity_id = clicked_button.getAttribute("value")

                const queryString = new URLSearchParams({activity_id}).toString();

                fetch(`/api/delete_activity?${queryString}`)
                    .then((response) => response.json())
                    .then((data) => {
                        alert(data.status);
                        document.location.reload();
                    })
                .catch(() => {
                    alert('Something went wrong! Unable to delete activity.')
                })
                
            });
        }
    })
    .catch(() => {
        alert('Something wrong with the database!')
    })