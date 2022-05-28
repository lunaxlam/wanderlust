'use strict';

function AddDestinationContainer() {

    const onClick = () => {

        fetch('/api/session_itinerary')
            .then((res) => res.json())
            .then((data) => {

                const itinerary_id = data

                if (document.querySelector('#add-destination-form').innerHTML === '') {

                    document.querySelector('#add-destination-form').innerHTML =
                    `<form action='/itinerary/${itinerary_id}/add_destination' class='active-form'>
                    <label for='destination-locale'>Locale:</label>
                    <input type='text' name='locale' id='destination-locale' required>
                    <br>
                    <label for='destination-territory'>Territory</label>
                    <input type='text' name='territory' id='destination-territory' required>
                    <br>
                    <label for='destination-country'>Country</label>
                    <input type='text' name='country' id='destination-country' pattern='(\\b\\w{3}\\b)' required>
                    <br>
                    <p class='hint'>Country code must be entered as three-letter 
                        <a href='https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3' 
                            target='_blank'>ISO-3166</a> code standard. Need a 
                        <a href='/countries' target='_blank'>hint</a>?</p>
                    <input type='submit' name='submit'>
                </form>`
            
                } else {
            
                    document.querySelector('#add-destination-form').innerHTML = ''
            
                }

            })

    }
    return (
        <button onClick={onClick}>Add Destination</button>
    );
}

ReactDOM.render(<AddDestinationContainer />, document.querySelector('#add-destination-btn'));