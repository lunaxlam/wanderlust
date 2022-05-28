'use strict';

function LogIn() {

    const onClick = () => {

        document.querySelector('#display-form').innerHTML =
            `<form action='/login' method="POST" class='active-form'>
                <label for='user-email'>Email: </label>
                <input type='email' name='email' id='user-email'>
                <br>
                <label for='user-password'>Password: </label>
                <input type='password' name='password' id='user-password'>
                <br>
                <input type='submit'>
            </form>`
    }
    return (
        <button onClick={onClick}>Log-In</button>
    );
}

ReactDOM.render(<LogIn />, document.querySelector('#log-in'));
