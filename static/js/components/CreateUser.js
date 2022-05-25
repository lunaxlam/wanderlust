'use strict';

function CreateUser() {

    const onClick = (evt) => {

        const Btn = evt.target;

        Btn.hidden = true;

        document.querySelector('#create-user').insertAdjacentHTML(
            'beforeend',
            `<h2>Create Account</h2>
            <form action='/create_user' method='POST' class='active-form'>
                <label for='user-username'>Username: </label>
                <input type='text' name='username' id='user-username' required>
                <br>
                <label for='user-password'>Password: </label>
                <input type='password' name='password' id='user-password' required>
                <br>
                <label for='user-fname'>First Name: </label>
                <input type='text' name='fname' id='user-fname' required>
                <br>
                <label for='user-lname'>Last Name: </label>
                <input type='text' name='lname' id='user-lname' required>
                <br>
                <label for='user-email'>Email: </label>
                <input type='email' name='email' id='user-email' pattern='(\\w+|\\d+)\\@(\\w+|\\d+).' required>
                <br>
                <label for='user-locale'>Locale: </label>
                <input type='text' name='locale' id='user-locale' required>
                <br>
                <label for='user-territory'>Territory: </label>
                <input type='text' name='territory' id='user-territory' required>
                <br>
                <label for='user-country'>Country: </label>
                <input type='text' name='country' id='destination-country' pattern='(\\b\\w{3}\\b)' required>
                <br>
                <p class='hint'>Country code must be entered as three-letter 
                    <a href='https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3' 
                        target='_blank'>ISO-3166</a> code standard. Need a 
                    <a href='/countries' target='_blank'>hint</a>?</p>
                <label for='user-about-me'>Bio: </label>
                <textarea name='about_me' id='user-about-me'></textarea>
                <br>
                <input type='submit' name='submit' required>
            </form>`
        )
    }
    return (
        <button onClick={onClick}>Create Account</button>
    );
}

ReactDOM.render(<CreateUser />, document.querySelector('#create-user'));
