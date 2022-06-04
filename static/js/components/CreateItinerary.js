'use strict';

function CreateItinerary() {

    const onClick = () => {

        if (document.querySelector('#mount-itinerary').innerHTML === '') {

            document.querySelector('#mount-itinerary').innerHTML =
            `<form class='row g-3 sub-main' action='/create_itinerary' method='POST'>
                <div class='col-md-12'>
                    <label for='itinerary-name' class='form-label'>Name</label>
                    <input type='text' class='form-control' name='name' id='itinerary-name' required>
                </div>
                <div class='col-md-12'>
                    <label for='itinerary-locale' class='form-label'>Locale</label>
                    <input type='text' class='form-control' name='locale' id='itinerary-locale' required>
                </div>
                <div class='col-md-12'>
                    <label for='itinerary-territory' class='form-label'>Territory</label>
                    <input type='text' class='form-control' name='territory' id='itinerary-territory' required>
                </div>
                <div class='col-md-12'>
                    <label for='itinerary-country' class='form-label'>Country</label>
                    <input type='text' class='form-control' name='country' id='destination-country' pattern='\\b[a-zA-Z]{3}\\b' required>
                    <p class='hint'>Country code must be entered as three-letter 
                        <a href='https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3' 
                            target='_blank'>ISO-3166</a> code standard. Need a 
                        <a href='/countries' target='_blank'>hint</a>?
                    </p>
                </div>
                <div class='col-md-12'>
                    <label for='itinerary-overview' class='form-label'>Overview</label>
                    <input type='text' class='form-control' name='overview' id='itinerary-overview' required>
                </div>
                <div class='col-12'>
                    <button type='submit' class='btn btn-primary btn-sm'>Submit</button>
                </div>
            </form>`

        } else {
            document.querySelector('#mount-itinerary').innerHTML = '';
        }

    }
    return (
        <button onClick={onClick} className="btn btn-secondary btn-sm">Plan Trip</button>
    );
}

ReactDOM.render(<CreateItinerary />, document.querySelector('#create-itinerary'));