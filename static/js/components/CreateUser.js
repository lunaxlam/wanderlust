'use strict';

function CreateUser() {

    const onClick = () => {

        document.querySelector('#display-form').innerHTML =
            `<form class='row g-3' action='/create_user' method='POST'>
                <div class='col-md-6'>
                    <label for='user-email' class='form-label'>Email</label>
                    <input type='email' class='form-control' name='email' id='user-email' pattern='(\\w+|\\d+)\\@(\\w+|\\d+).' required>
                </div>
                <div class='col-md-6'>
                    <label for='user-password' class='form-label'>Password</label>
                    <input type='password' class='form-control' name='password' id='user-password'>
                </div>
                <div class='col-md-6'>
                    <label for='user-fname' class='form-label'>First Name</label>
                    <input type='text' class='form-control' name='fname' id='user-fname'>
                </div>
                <div class='col-md-6'>
                    <label for='user-lname' class='form-label'>Last Name</label>
                    <input type='text' class='form-control' name='lname' id='user-lname'>
                </div>
                <div class='col-md-6'>
                    <label for='user-locale' class='form-label'>Locale</label>
                    <input type='text' class='form-control' name='locale' id='user-locale'>
                </div>
                <div class='col-md-6'>
                    <label for='user-territory' class='form-label'>Territory</label>
                    <input type='text' class='form-control' name='territory' id='user-territory'>
                </div>
                <div class='col-md-6'>
                    <label for='user-country' class='form-label'>Country</label>
                    <input type='text' class='form-control' name='country' id='destination-country' pattern='(\\b\\w{3}\\b)' required>
                    <p class='hint'>Country code must be entered as three-letter 
                        <a href='https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3' 
                            target='_blank'>ISO-3166</a> code standard. Need a 
                        <a href='/countries' target='_blank'>hint</a>?
                    </p>
                </div>
                <div class='col-md-6'>
                    <label for='user-username' class='form-label'>Select Username</label>
                    <input type='text' class='form-control' name='username' id='user-username'>
                </div>
                <div class='col-md-12'>
                    <label for='user-aboutme' class='form-label'>About Me</label>
                    <textarea class='form-control' name='about_me' id='user-about-me'></textarea>
                </div>
                <div class='col-12'>
                    <button type='submit' class='btn btn-primary'>Sign Up</button>
                </div>
            </form>`
    }
    return (
        <button onClick={onClick}>Create Account</button>
    );
}

ReactDOM.render(<CreateUser />, document.querySelector('#create-user'));

