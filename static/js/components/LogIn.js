'use strict';

function LogIn() {

    const onClick = (evt) => {

        const Btn = evt.target;

        Btn.hidden = true;

        document.querySelector('#log-in').insertAdjacentHTML(
            'beforeend',
            `<h2>Log-In</h2>
            <form action='/login' method="POST">
                <label for='user-email'>Email: </label>
                <input type='email' name='email' id='user-email'>
                <br>
                <label for='user-password'>Password: </label>
                <input type='password' name='password' id='user-password'>
                <br>
                <input type='submit'>
            </form>`
        )
    }
    return (
        <button onClick={onClick}>Log-In</button>
    );
}

ReactDOM.render(<LogIn />, document.querySelector('#log-in'));
