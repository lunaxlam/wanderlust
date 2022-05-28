'use strict';

function CloneItineraryContainer() {

    const onClick = () => {

        fetch('/api/session_itinerary')
            .then((res) => res.json())
            .then((data) => {

                const itinerary_id = data

                if (document.querySelector('#clone-trip-form').innerHTML === '') {

                    document.querySelector('#clone-trip-form').innerHTML =
                    `<form action='/itinerary/${itinerary_id}', method='POST'>
                        <label for='itinerary-name'>Name Your Trip: </label>
                        <input type='text' name='name' id='itinerary-name' required>
                        <br>
                        <label for='itinerary-overview'>Overview: </label>
                        <input type='text' name='overview' id='itinerary-overview' required>
                        <br>
                        <input type='submit' name='submit'>
                    </form>`
            
                } else {
            
                    document.querySelector('#clone-trip-form').innerHTML = ''
            
                }

            })

    }
    return (
        <button onClick={onClick}>Clone This Trip</button>
    );
}

ReactDOM.render(<CloneItineraryContainer />, document.querySelector('#clone-trip-btn'));