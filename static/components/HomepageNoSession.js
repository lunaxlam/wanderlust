function HomepageNoSession() {
    return (
        <React.Fragment>
            <h1>Welcome to Wanderlust!</h1>
            <h2 class="start">Adventure awaits...</h2>
            <ul class="start"><a href="/login">Log-in</a></ul>
            <ul class="start"><a href="/create_user">Create an account</a></ul>        
        </React.Fragment>
    );
}

ReactDOM.render(<HomepageNoSession />, document.querySelector('#no-session'));