'use strict';

function Activity( { dates, start, end, location, url, formattedAddress, phone, notes, activityID, itineraryID }) {

    const deleteActivity = (evt) => {

        const deleteButton = evt.target;

        const activityID = deleteButton.getAttribute('value');

        const queryString = new URLSearchParams({activityID}).toString();

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

    const editActivity = (evt) => {

        const editButton = evt.target;

        const activityID = editButton.getAttribute('value');

        document.querySelector(`#edit-activity-form${activityID}`).innerHTML =
        `<div class='edit-activity-container'>
            <form class="row g-3 sub-main" action="/itinerary/${itineraryID}/edit_activity/${activityID}" method="POST">
                <h5 class="">Edit Activity at ${location}</h5><br>            
                <div class="col-md-6">
                    <label for="activity-start" class="form-label lb-lg">Start</label>
                    <input type="datetime-local" class="form-control" name="start" id="activity-start">
                </div>
                <div class="col-md-6">
                    <label for="activity-end" class="form-label lb-lg">End</label>
                    <input type="datetime-local" class="form-control" name="end" id="activity-end">
                </div>
                <div class="col-md-12">
                    <label for="activity-notes" class="form-label lb-lg">Activity Notes</label>
                    <textarea name="notes" id="activity-notes" class="form-control lb-lg"></textarea>
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-outline-danger">Update</button>
                </div>
            </form>
        </div>`
    }

    if (notes === '') {

        return (
            <ul>
                <button onClick={deleteActivity} 
                    id='delete' 
                    value={activityID}
                    className='btn btn-danger btn-sm fa fa-close'>
                </button>
                <li className='main-heading'>{location} </li>    
                <li className='main-heading'>{dates} </li> 
                <li>Start: {start} </li> 
                <li>End: {end} </li>       
                <li>Address: <a href={url} target='_blank' rel='noopener noreferrer'>{formattedAddress}</a></li>
                <li>Phone: {phone} </li>
                <br />
                <button 
                    onClick={editActivity}
                    value= {activityID}
                    className='btn btn-outline-danger btn-sm'
                    data-bs-target={`#edit-activity-form${activityID}`}
                    data-bs-toggle='collapse'>
                        Edit Activity
                </button>
                <div id={`edit-activity-form${activityID}`}></div>
            </ul>
        );

    } else {

        return (
            <div className='container saved-activity'>
                <ul>
                    <button onClick={deleteActivity} 
                        id='delete' 
                        value={activityID}
                        className='btn btn-danger btn-sm fa fa-close'>
                    </button>
                    <li className='main-heading'>{location} </li>    
                    <li className='main-heading'>{dates} </li> 
                    <li>Start: {start} </li> 
                    <li>End: {end} </li>       
                    <li>Address: <a href={url} target='_blank' rel='noopener noreferrer'>{formattedAddress}</a></li>
                    <li>Phone: {phone} </li>
                    <li>Notes: {notes} </li>
                    <br />
                    <button 
                        onClick={editActivity}
                        value= {activityID}
                        className='btn btn-outline-danger btn-sm'
                        data-bs-target={`#edit-activity-form${activityID}`}
                        data-bs-toggle='collapse'>
                            Edit Activity
                    </button>
                    <div id={`edit-activity-form${activityID}`}></div>
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
            alert('Oh no! The Google API trial period has ended for this application.')
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
                itineraryID={activities[i]['itinerary_id']}
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