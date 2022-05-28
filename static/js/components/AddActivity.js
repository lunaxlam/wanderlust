'use strict';

function AddActivityContainer() {

    const onClick = () => {

        fetch('/api/search_place_data')
            .then((res) => res.json())
            .then((data) => {

                const itineraryID = data["itinerary_id"]
                const placeID =  data["place_id"]

                if (document.querySelector('#add-activity-form').innerHTML === '') {

                    document.querySelector('#add-activity-form').innerHTML =
                    `<form action='/itinerary/${itineraryID}/${placeID}/add_activity'>
                    <label for='activity-start'>Start:</label>
                    <input type='datetime-local' name='start' id='activity-start'><br>
                    <label for='activity-end'>End:</label>
                    <input type='datetime-local' name='end' id='activity-end'><br>
                    <label for='activity-notes'>Notes:</label>
                    <textarea name='notes' id='activity-notes'></textarea><br>
                    <input type='submit' name='submit'>
                </form>`
            
                } else {
            
                    document.querySelector('#add-destination-form').innerHTML = ''
            
                }

            })

    }
    return (
        <button onClick={onClick}>Add Activity</button>
    );
}

ReactDOM.render(<AddActivityContainer />, document.querySelector('#add-activity-btn'));