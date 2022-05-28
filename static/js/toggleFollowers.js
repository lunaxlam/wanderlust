'use strict';

// Event Listeners to toggle Followers & Following

const followersBtn = document.querySelector('#my-followers-btn');
const myFollowers = document.querySelector('#my-followers');

const followingBtn = document.querySelector('#following-btn');
const following = document.querySelector('#following');


followersBtn.addEventListener('click', () => {
    if (myFollowers.style.display === "") {
        myFollowers.style.display = "block";
        following.style.display = "";
    } else {
        myFollowers.style.display = "";
    }

})


followingBtn.addEventListener('click', () => {

    if (following.style.display === "") {
        following.style.display = "block";
        myFollowers.style.display = "";
    } else {
        following.style.display = "";
    }

})

