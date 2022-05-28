'use strict';

function CreateItinerary() {

    const onClick = (evt) => {

        if (document.querySelector('#mount-itinerary').innerHTML === '') {

            document.querySelector('#mount-itinerary').innerHTML =
            `<form action='/create_itinerary' method='POST' class='active-form'>
                <label for='itinerary-name'>Name Your Trip: </label>
                <input type='text' name='name' id='itinerary-name' required>
                <br>
                <label for='itinerary-overview'>Overview: </label>
                <input type='text' name='overview' id='itinerary-overview' required>
                <br>
                <label for='destination-locale'>Locale: </label>
                <input type='text' name='locale' id='itinerary-locale' required>
                <br>
                <label for='destination-territory'>Territory: </label>
                <input type='text' name='territory' id='itinerary-territory' required>
                <br>
                <label for='destionation-country'>Country: </label>
                <input type='text' name='country' id='destination-country' pattern='(\\b\\w{3}\\b)' required>
                <br>
                <p class='hint'>Country code must be entered as three-letter 
                    <a href='https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3' 
                        target='_blank'>ISO-3166</a> code standard. Need a 
                    <a href='/countries' target='_blank'>hint</a>?</p>
                <input type='submit' name='submit'>
            </form>`

        } else {
            document.querySelector('#mount-itinerary').innerHTML = '';
        }

    }
    return (
        <button onClick={onClick}>Plan A New Adventure</button>
    );
}

ReactDOM.render(<CreateItinerary />, document.querySelector('#create-itinerary'));