'use strict';

function Activity( { dates, start, end, location, url, formattedAddress, phone, notes, activityID }) {

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

    if (notes === '') {

        return (
            <ul>
                <li className='main-heading'>{location} </li>    
                <li className='main-heading'>{dates} </li> 
                <li>Start: {start} </li> 
                <li>End: {end} </li>       
                <li>Address: <a href={url} target='_blank' rel='noopener noreferrer'>{formattedAddress}</a></li>
                <li>Phone: {phone} </li>
                <button onClick={onClick} 
                    id='delete' 
                    value={activityID}>Delete
                </button>
                <br /><br />
            </ul>
        );

    } else {

        return (
            <div className="container saved-activity">
                <ul>
                    <li class="activity-heading">{location} </li>    
                    <li class="activity-heading">{dates} </li> 
                    <li>Start: {start} </li> 
                    <li>End: {end} </li>       
                    <li>Address: <a href={url} target='_blank' rel='noopener noreferrer'>{formattedAddress}</a></li>
                    <li>Phone: {phone} </li>
                    <li>Notes: {notes} </li>
                    <button onClick={onClick} 
                        id='delete' 
                        value={activityID}
                        class="btn btn-danger btn-sm">Delete
                    </button>
                    <br /><br />
                </ul>
            </div>
        );

    } 
}

function ActivitiesContainer() {
    
    const [activities, setActivities] = React.useState([]);

    React.useEffect(() => {
        fetch('/api/saved_activities')
        .then((res) => res.json())
        .catch(() => {
            alert('Something wrong with the route!')
        })
        .then((data) => {

            if ('0' in data) {
                setActivities(data)
            }
    
        })
    }, [])

    const allActivities = []

    for (const i in activities) {

        let phone = activities[i]['results']['formatted_phone_number'];

        if (typeof phone === 'undefined') {
            phone = 'Not listed.'
        }

        allActivities.push(
            <Activity 
                key={i}
                location={activities[i]['results']['name']}
                dates={activities[i]['dates']}
                start={activities[i]['start']}
                end={activities[i]['end']}
                url={activities[i]['results']['url']}
                formattedAddress={activities[i]['results']['formatted_address']}
                phone={phone}
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

ReactDOM.render(<ActivitiesContainer />, document.querySelector('#saved-activities'));