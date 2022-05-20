function HomepageInSession() {
    return (
        <React.Fragment>
            <h1>Where will adventure take you?</h1>
            <ul class="start"><a href="/itineraries">View Wanderlust Travel Itineraries</a></ul>
            <ul class="start"><a href="/create_itinerary">Create a New Travel Itinerary</a></ul>
        </React.Fragment>
    );
}

ReactDOM.render(<HomepageInSession />, document.querySelector('#in-session'));