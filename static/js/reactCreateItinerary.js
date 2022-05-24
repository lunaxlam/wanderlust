'use strict';

function CreateItinerary() {

    const onClick = (evt) => {

        const Btn = evt.target;

        Btn.hidden = true;

        document.querySelector('#create-itinerary').insertAdjacentHTML(
            'beforeend',
            `<h2>Plan A New Adventure</h2>
            <form action='/create_itinerary' method='POST'>
                <label for='itinerary-name'>Name Your Trip: </label>
                <input type='text' name='name' id='itinerary-name' required>
                <br>
                <label for='itinerary-overview'>Brief Description: </label>
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
                <input type="submit" name="submit">
            </form>`
        )
    }
    return (
        <button onClick={onClick}>Plan A New Adventure</button>
    );
}

ReactDOM.render(<CreateItinerary />, document.querySelector('#create-itinerary'));