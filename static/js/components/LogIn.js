'use strict';

function LogIn() {

    const onClick = () => {

        document.querySelector('#display-form').innerHTML =
            `<form class='row g-3' action='/login' method='POST'>
                <div class='col-md-6'>
                    <label for='user-email' class='form-label'>Email</label>
                    <input type='email' class='form-control' name='email' id='user-email'>
                </div>
                <div class='col-md-6'>
                    <label for='user-password' class='form-label'>Password</label>
                    <input type='password' class='form-control' name='password' id='user-password'>
                </div>
                <div class='col-12'>
                    <button type='submit' class='btn btn-primary'>Sign in</button>
                </div>
            </form>`
    }
    return (
        <button onClick={onClick}>Log-In</button>
    );
}

ReactDOM.render(<LogIn />, document.querySelector('#log-in'));

