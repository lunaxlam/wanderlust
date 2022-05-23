function Itinerary({ itinerary_id, itinerary_name }) {
    return (
        <ul><a href={`/itinerary/${itinerary_id}`} target='blank'>Itinerary ID: {itinerary_id}, {itinerary_name}</a></ul>
    );
}

function AllItineraries() {

    const [itineraries, setItineraries] = React.useState([]);

    React.useEffect(() => {
        fetch('/all_itineraries.json')
        .then(response => response.json())
        .then(data => setItineraries(data))
    }, [])

    const allItineraries = []

    for (const itinerary in itineraries) {
        allItineraries.push(
            <Itinerary 
                key={itineraries[itinerary]["itinerary_id"]}
                itinerary_id={itineraries[itinerary]["itinerary_id"]}
                itinerary_name={itineraries[itinerary]["itinerary_name"]}
            />,
        );
    }
    return (
        <React.Fragment>
            {allItineraries}
        </React.Fragment>
    );
}

ReactDOM.render(<AllItineraries />, document.querySelector('#all-itineraries'));