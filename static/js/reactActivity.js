'use strict';

function Activity( { name, dates, start, end, location, url, formattedAddress, phone, notes, activityID }) {

    const onClick = (evt) => {
        const clicked_button = evt.target;

        const activity_id = clicked_button.getAttribute("value");

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
    }
    return (
        <section>
            <ul>Name: {name} </ul>
            <ul>Dates: {dates} </ul> 
            <ul>Start: {start} </ul> 
            <ul>End: {end} </ul>   
            <ul>Location: {location} </ul>                    
            <ul>Address: <a href={url} target='blank'>{formattedAddress}</a></ul>
            <ul>Phone: {phone} </ul>
            <ul>Notes: {notes} </ul>
            <button onClick={onClick} 
                id='delete' 
                value={activityID}>Delete Activity
            </button>
            <br /><br />
        </section>
    );
}

function ActivitiesContainer() {
    
    const [activities, setActivities] = React.useState([]);

    React.useEffect(() => {
        fetch('/api/saved_activities')
        .then((res) => res.json())
        .catch(() => {
            alert('Something wrong with the route!')
        })
        .then(data => setActivities(data))
    }, [])

    const allActivities = []

    for (const i in activities) {

        allActivities.push(
            <Activity 
                key={i}
                name={activities[i]['activity_name']}
                dates={activities[i]['dates']}
                start={activities[i]['start']}
                end={activities[i]['end']}
                location={activities[i]['results']['name']}
                url={activities[i]['results']['url']}
                formattedAddress={activities[i]['results']['formatted_address']}
                phone={activities[i]['results']['formatted_phone_number']}
                notes={activities[i]['notes']}
                activityID={activities[i]['activity_id']}
            />
        )
    }
    return (
        <React.Fragment>
            {allActivities}
        </React.Fragment>
    );
}

ReactDOM.render(<ActivitiesContainer />, document.querySelector('#saved-place'));