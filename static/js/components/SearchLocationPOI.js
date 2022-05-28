'use strict';

function SearchPOI() {

    const onClick = () => {

        fetch('/api/session_itinerary')
            .then((res) => res.json())
            .then((data) => {

                const itinerary_id = data

                if (document.querySelector('#display-search-form').innerHTML === '') {

                    document.querySelector('#display-autocomplete-form').hidden = true;

                    document.querySelector('#display-search-form').innerHTML =
                    `<form action="/itinerary/${itinerary_id}/search">
                        <label for="search-keyword">Description:</label>
                        <input type="text" name="keyword" id="search-keyword" size="40" placeholder="Italian Restaurants">
                        <br>
                        <label for="search-location">Location:</label>
                        <input type="text" name="location" id="search-location" placeholder="Chicago">
                        <br>
                        <input type="submit" name="submit">
                    </form>`

                } else {
                    
                    document.querySelector('#display-search-form').innerHTML = ''

                }

            })

    }
    return (
        <button onClick={onClick}>By Point of Interest</button>
    );
}

ReactDOM.render(<SearchPOI />, document.querySelector('#search-poi'));